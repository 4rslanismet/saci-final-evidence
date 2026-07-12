#!/usr/bin/env python3
"""Build and query a private local index from a ChatGPT data export.

The raw export remains outside the repository. The generated SQLite database is
written under .private/, which this project intentionally ignores in Git.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import mimetypes
import os
import re
import sqlite3
import sys
from collections import Counter
from contextlib import closing
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


SCHEMA_VERSION = "2"
INDEX_FORMAT_VERSION = "3"
PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DB = PROJECT_ROOT / ".private" / "chat-memory" / "index.sqlite3"
FILE_REF_RE = re.compile(r"(?<![A-Za-z0-9_-])(file[-_][A-Za-z0-9_-]{12,})")
HIDDEN_CONTENT_TYPES = {"thoughts", "reasoning_recap"}
VISIBLE_ROLES = {"user", "assistant"}


BASE_SCHEMA = """
CREATE TABLE archive_meta (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL
);

CREATE TABLE source_inputs (
    path TEXT PRIMARY KEY,
    size_bytes INTEGER NOT NULL,
    sha256 TEXT NOT NULL
);

CREATE TABLE archive_files (
    path TEXT PRIMARY KEY,
    expected_size_bytes INTEGER,
    actual_size_bytes INTEGER,
    exists_flag INTEGER NOT NULL,
    size_matches INTEGER NOT NULL
);

CREATE TABLE conversations (
    id TEXT PRIMARY KEY,
    kind TEXT NOT NULL,
    title TEXT NOT NULL,
    create_time REAL,
    update_time REAL,
    current_node TEXT,
    default_model_slug TEXT,
    is_archived INTEGER NOT NULL DEFAULT 0,
    is_starred INTEGER NOT NULL DEFAULT 0,
    is_do_not_remember INTEGER NOT NULL DEFAULT 0,
    is_shared INTEGER NOT NULL DEFAULT 0,
    source_file TEXT NOT NULL,
    message_count INTEGER NOT NULL DEFAULT 0,
    current_path_message_count INTEGER NOT NULL DEFAULT 0,
    metadata_json TEXT NOT NULL
);

CREATE INDEX conversations_time_idx ON conversations(update_time DESC);
CREATE INDEX conversations_kind_idx ON conversations(kind);

CREATE TABLE messages (
    row_id INTEGER PRIMARY KEY,
    conversation_id TEXT NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
    node_id TEXT NOT NULL,
    message_id TEXT,
    parent_node_id TEXT,
    role TEXT,
    author_name TEXT,
    create_time REAL,
    content_type TEXT,
    text TEXT NOT NULL,
    content_json TEXT NOT NULL,
    metadata_json TEXT NOT NULL,
    is_current_path INTEGER NOT NULL DEFAULT 0,
    path_order INTEGER,
    source_order INTEGER NOT NULL,
    UNIQUE(conversation_id, node_id)
);

CREATE INDEX messages_conversation_idx
    ON messages(conversation_id, is_current_path, path_order, source_order);
CREATE INDEX messages_time_idx ON messages(create_time DESC);
CREATE INDEX messages_role_idx ON messages(role);
CREATE INDEX messages_content_type_idx ON messages(content_type);

CREATE TABLE assets (
    export_filename TEXT PRIMARY KEY,
    original_filename TEXT,
    source_path TEXT NOT NULL,
    size_bytes INTEGER,
    exists_flag INTEGER NOT NULL,
    detected_mime TEXT,
    sha256 TEXT
);

CREATE TABLE message_assets (
    message_row_id INTEGER NOT NULL REFERENCES messages(row_id) ON DELETE CASCADE,
    reference TEXT NOT NULL,
    export_filename TEXT REFERENCES assets(export_filename),
    PRIMARY KEY(message_row_id, reference)
);

CREATE INDEX message_assets_export_idx ON message_assets(export_filename);

CREATE TABLE library_files (
    record_id TEXT PRIMARY KEY,
    file_id TEXT,
    export_filename TEXT REFERENCES assets(export_filename),
    file_name TEXT,
    mime_type TEXT,
    size_bytes INTEGER,
    initiating_conversation_id TEXT,
    origination_thread_id TEXT,
    origination_message_id TEXT,
    state TEXT,
    raw_json TEXT NOT NULL
);

CREATE INDEX library_files_file_id_idx ON library_files(file_id);
CREATE INDEX library_files_conversation_idx ON library_files(initiating_conversation_id);
CREATE INDEX library_files_thread_idx ON library_files(origination_thread_id);

CREATE TABLE shared_conversations (
    share_id TEXT PRIMARY KEY,
    conversation_id TEXT,
    title TEXT,
    is_anonymous INTEGER,
    raw_json TEXT NOT NULL
);
"""


def compact_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"), sort_keys=True)


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8-sig") as handle:
        return json.load(handle)


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def parse_time(value: Any) -> float | None:
    if isinstance(value, bool) or value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value)
    if not isinstance(value, str) or not value.strip():
        return None
    text = value.strip().replace("Z", "+00:00")
    try:
        parsed = datetime.fromisoformat(text)
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.timestamp()


def iso_time(value: float | None) -> str:
    if value is None:
        return "unknown-time"
    return datetime.fromtimestamp(value, tz=timezone.utc).isoformat().replace("+00:00", "Z")


def as_bool_int(value: Any) -> int:
    return 1 if bool(value) else 0


def scalar_identifier(value: Any) -> str | None:
    if isinstance(value, dict):
        value = value.get("id")
    if isinstance(value, (str, int)) and not isinstance(value, bool):
        text = str(value).strip()
        return text or None
    return None


def normalize_text(content: Any) -> str:
    pieces: list[str] = []

    def walk(value: Any) -> None:
        if isinstance(value, str):
            text = value.strip()
            if not text:
                return
            if text.startswith("data:") and len(text) > 512:
                pieces.append("[embedded binary data omitted]")
            else:
                pieces.append(text)
            return
        if isinstance(value, list):
            for item in value:
                walk(item)
            return
        if not isinstance(value, dict):
            return

        pointer = value.get("asset_pointer")
        if isinstance(pointer, str):
            match = FILE_REF_RE.search(pointer)
            pieces.append(f"[attachment: {match.group(1) if match else pointer}]")

        skipped = {
            "asset_pointer",
            "content_type",
            "mime_type",
            "size_bytes",
            "width",
            "height",
            "finished",
        }
        for key, item in value.items():
            if key not in skipped:
                walk(item)

    walk(content)
    result: list[str] = []
    for piece in pieces:
        if not result or result[-1] != piece:
            result.append(piece)
    return "\n\n".join(result)


def collect_file_references(value: Any) -> set[str]:
    references: set[str] = set()

    def walk(item: Any) -> None:
        if isinstance(item, str):
            references.update(match.group(1) for match in FILE_REF_RE.finditer(item))
        elif isinstance(item, list):
            for child in item:
                walk(child)
        elif isinstance(item, dict):
            for key, child in item.items():
                if key in {"asset_pointer", "file_id", "target_id", "attachment_id"}:
                    if isinstance(child, str) and child.strip():
                        match = FILE_REF_RE.search(child)
                        references.add(match.group(1) if match else child.strip())
                walk(child)

    walk(value)
    return references


def collect_attachment_labels(value: Any) -> list[str]:
    labels: list[str] = []

    def walk(item: Any) -> None:
        if isinstance(item, list):
            for child in item:
                walk(child)
            return
        if not isinstance(item, dict):
            return
        is_attachment = any(
            key in item for key in ("asset_pointer", "file_id", "target_id", "attachment_id")
        )
        if is_attachment:
            found_label = False
            for key in ("title", "name", "file_name", "filename", "type", "mime_type"):
                label = item.get(key)
                if isinstance(label, str) and label.strip():
                    labels.append(label.strip())
                    found_label = True
            if not found_label:
                for key in ("target_id", "file_id", "asset_pointer", "attachment_id"):
                    label = item.get(key)
                    if isinstance(label, str) and label.strip():
                        labels.append(label.strip())
                        break
        for child in item.values():
            walk(child)

    walk(value)
    return list(dict.fromkeys(labels))


def detect_mime(path: Path, original_filename: str | None) -> str | None:
    try:
        with path.open("rb") as handle:
            head = handle.read(512)
    except OSError:
        return None

    signatures = (
        (b"\x89PNG\r\n\x1a\n", "image/png"),
        (b"\xff\xd8\xff", "image/jpeg"),
        (b"GIF87a", "image/gif"),
        (b"GIF89a", "image/gif"),
        (b"%PDF-", "application/pdf"),
        (b"\x1f\x8b", "application/gzip"),
        (b"RIFF", "application/riff"),
        (b"OggS", "application/ogg"),
        (b"ID3", "audio/mpeg"),
        (b"SQLite format 3\x00", "application/vnd.sqlite3"),
    )
    for signature, mime in signatures:
        if head.startswith(signature):
            if signature == b"RIFF" and head[8:12] == b"WEBP":
                return "image/webp"
            if signature == b"RIFF" and head[8:12] == b"WAVE":
                return "audio/wav"
            return mime
    if head.startswith(b"PK\x03\x04"):
        zip_container_mimes = {
            ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            ".xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            ".pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
            ".epub": "application/epub+zip",
            ".sdocx": "application/x-sdocx",
        }
        suffix = Path(original_filename or "").suffix.casefold()
        return zip_container_mimes.get(suffix, "application/zip")
    if len(head) >= 12 and head[4:8] == b"ftyp":
        return "video/mp4"

    guessed = mimetypes.guess_type(original_filename or "")[0]
    if guessed:
        return guessed
    if head and b"\x00" not in head:
        try:
            head.decode("utf-8")
            return "text/plain"
        except UnicodeDecodeError:
            pass
    return "application/octet-stream"


def resolve_asset(reference: str, asset_names: set[str]) -> str | None:
    candidates = [reference, f"{reference}.dat"]
    basename = Path(reference).name
    candidates.extend([basename, f"{basename}.dat"])
    for candidate in candidates:
        if candidate in asset_names:
            return candidate
    return None


def connect_database(path: Path) -> sqlite3.Connection:
    connection = sqlite3.connect(path)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    connection.create_function(
        "casefold",
        1,
        lambda value: value.casefold() if isinstance(value, str) else "",
        deterministic=True,
    )
    return connection


def set_meta(connection: sqlite3.Connection, key: str, value: Any) -> None:
    if not isinstance(value, str):
        value = compact_json(value)
    connection.execute(
        "INSERT OR REPLACE INTO archive_meta(key, value) VALUES (?, ?)",
        (key, value),
    )


def create_schema(connection: sqlite3.Connection) -> bool:
    connection.executescript(BASE_SCHEMA)
    try:
        connection.execute(
            """
            CREATE VIRTUAL TABLE message_fts USING fts5(
                title,
                text,
                attachments,
                conversation_id UNINDEXED,
                role UNINDEXED,
                tokenize='unicode61 remove_diacritics 2'
            )
            """
        )
    except sqlite3.OperationalError:
        return False
    return True


def record_source_input(connection: sqlite3.Connection, source: Path, relative: str) -> str:
    path = source / relative
    digest = file_sha256(path)
    connection.execute(
        "INSERT INTO source_inputs(path, size_bytes, sha256) VALUES (?, ?, ?)",
        (relative.replace("\\", "/"), path.stat().st_size, digest),
    )
    return digest


def insert_message(
    connection: sqlite3.Connection,
    *,
    fts_enabled: bool,
    conversation_id: str,
    title: str,
    node_id: str,
    message_id: str | None,
    parent_node_id: str | None,
    role: str | None,
    author_name: str | None,
    create_time: float | None,
    content_type: str | None,
    content: Any,
    metadata: Any,
    is_current_path: int,
    path_order: int | None,
    source_order: int,
    asset_names: set[str],
    asset_original_names: dict[str, str | None],
) -> int:
    text = normalize_text(content)
    references = collect_file_references({"content": content, "metadata": metadata})
    resolved_assets: list[tuple[str, str | None]] = []
    attachment_labels: list[str] = collect_attachment_labels(metadata)
    for reference in sorted(references):
        export_filename = resolve_asset(reference, asset_names)
        resolved_assets.append((reference, export_filename))
        if export_filename:
            attachment_labels.append(asset_original_names.get(export_filename) or export_filename)
    attachment_labels = list(dict.fromkeys(attachment_labels))

    cursor = connection.execute(
        """
        INSERT INTO messages(
            conversation_id, node_id, message_id, parent_node_id, role, author_name,
            create_time, content_type, text, content_json, metadata_json,
            is_current_path, path_order, source_order
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            conversation_id,
            node_id,
            message_id,
            parent_node_id,
            role,
            author_name,
            create_time,
            content_type,
            text,
            compact_json(content),
            compact_json(metadata),
            is_current_path,
            path_order,
            source_order,
        ),
    )
    row_id = int(cursor.lastrowid)
    for reference, export_filename in resolved_assets:
        connection.execute(
            "INSERT INTO message_assets(message_row_id, reference, export_filename) VALUES (?, ?, ?)",
            (row_id, reference, export_filename),
        )
    if fts_enabled:
        connection.execute(
            "INSERT INTO message_fts(rowid, title, text, attachments, conversation_id, role) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (row_id, title, text, "\n".join(attachment_labels), conversation_id, role),
        )
    return row_id


def current_path(mapping: dict[str, Any], current_node: Any) -> tuple[list[str], bool]:
    lineage: list[str] = []
    seen: set[str] = set()
    node_id = current_node if isinstance(current_node, str) else None
    cycle = False
    while node_id and node_id in mapping:
        if node_id in seen:
            cycle = True
            break
        seen.add(node_id)
        lineage.append(node_id)
        parent = mapping[node_id].get("parent")
        node_id = parent if isinstance(parent, str) else None
    lineage.reverse()
    return lineage, cycle


def build_database(source: Path, database_path: Path, hash_assets: bool) -> dict[str, Any]:
    manifest_path = source / "export_manifest.json"
    if not manifest_path.is_file():
        raise FileNotFoundError(f"Missing export manifest: {manifest_path}")
    manifest = load_json(manifest_path)
    logical = manifest.get("logical_files", {}).get("conversations.json", {})
    shard_names = logical.get("files", [])
    if not isinstance(shard_names, list) or not shard_names:
        raise ValueError("The manifest does not declare conversation shards")
    shard_names = [name for name in shard_names if isinstance(name, str)]

    connection = connect_database(database_path)
    connection.execute("PRAGMA journal_mode = OFF")
    connection.execute("PRAGMA synchronous = OFF")
    connection.execute("PRAGMA temp_store = MEMORY")
    fts_enabled = create_schema(connection)

    counters: Counter[str] = Counter()
    content_types: Counter[str] = Counter()
    roles: Counter[str] = Counter()
    source_hashes: list[str] = []
    asset_hashes: list[str] = []
    importer_digest = file_sha256(Path(__file__).resolve())

    try:
        source_hashes.append(record_source_input(connection, source, "export_manifest.json"))
        for optional_name in (
            "conversation_asset_file_names.json",
            "group_chats.json",
            "library_files.json",
            "shared_conversations.json",
        ):
            if (source / optional_name).is_file():
                source_hashes.append(record_source_input(connection, source, optional_name))
        for shard_name in shard_names:
            source_hashes.append(record_source_input(connection, source, shard_name))

        for entry in manifest.get("export_files", []):
            if not isinstance(entry, dict) or not isinstance(entry.get("path"), str):
                continue
            relative = entry["path"].replace("/", os.sep)
            physical = source / relative
            exists = physical.is_file()
            expected = entry.get("size_bytes")
            actual = physical.stat().st_size if exists else None
            size_matches = exists and (expected is None or actual == expected)
            connection.execute(
                "INSERT INTO archive_files VALUES (?, ?, ?, ?, ?)",
                (entry["path"], expected, actual, as_bool_int(exists), as_bool_int(size_matches)),
            )
            counters["manifest_files"] += 1
            counters["manifest_missing"] += 0 if exists else 1
            counters["manifest_size_mismatches"] += 0 if size_matches else 1

        asset_map_path = source / "conversation_asset_file_names.json"
        asset_map = load_json(asset_map_path) if asset_map_path.is_file() else {}
        if not isinstance(asset_map, dict):
            asset_map = {}
        asset_names: set[str] = set()
        asset_original_names: dict[str, str | None] = {}
        export_entries = {
            entry.get("path"): entry
            for entry in manifest.get("export_files", [])
            if isinstance(entry, dict) and isinstance(entry.get("path"), str)
        }
        dat_names = sorted(name for name in export_entries if name.lower().endswith(".dat"))
        for export_filename in dat_names:
            physical = source / export_filename.replace("/", os.sep)
            original = asset_map.get(export_filename)
            if not isinstance(original, str):
                original = None
            exists = physical.is_file()
            size = physical.stat().st_size if exists else None
            mime = detect_mime(physical, original) if exists else None
            digest = file_sha256(physical) if exists and hash_assets else None
            if digest:
                asset_hashes.append(digest)
            connection.execute(
                "INSERT INTO assets VALUES (?, ?, ?, ?, ?, ?, ?)",
                (export_filename, original, str(physical.resolve()), size, as_bool_int(exists), mime, digest),
            )
            asset_names.add(export_filename)
            asset_original_names[export_filename] = original
            counters["assets"] += 1
            counters["asset_bytes"] += size or 0
            counters["asset_missing"] += 0 if exists else 1
            counters["asset_mapped"] += 1 if original else 0

        library_path = source / "library_files.json"
        library_records = load_json(library_path) if library_path.is_file() else []
        if not isinstance(library_records, list):
            library_records = []
        for index, record in enumerate(library_records):
            if not isinstance(record, dict):
                continue
            file_id = scalar_identifier(record.get("file_id"))
            record_id = (
                scalar_identifier(record.get("id"))
                or file_id
                or f"library:{index}"
            )
            file_name = record.get("file_name")
            initiating_conversation_id = scalar_identifier(
                record.get("initiating_conversation_id")
            )
            origination_thread_id = scalar_identifier(record.get("origination_thread_id"))
            origination_message_id = scalar_identifier(record.get("origination_message_id"))
            export_filename = None
            for possible_id in (file_id, record_id):
                if possible_id:
                    export_filename = resolve_asset(possible_id, asset_names)
                    if export_filename:
                        break
            connection.execute(
                "INSERT OR REPLACE INTO library_files VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    record_id,
                    file_id,
                    export_filename,
                    file_name,
                    record.get("mime_type"),
                    record.get("file_size_bytes"),
                    initiating_conversation_id,
                    origination_thread_id,
                    origination_message_id,
                    record.get("state"),
                    compact_json(record),
                ),
            )
            if export_filename and isinstance(file_name, str):
                connection.execute(
                    "UPDATE assets SET original_filename = COALESCE(original_filename, ?) "
                    "WHERE export_filename = ?",
                    (file_name, export_filename),
                )
                if not asset_original_names.get(export_filename):
                    asset_original_names[export_filename] = file_name
            counters["library_records"] += 1

        # Library-only assets receive their display names after the first asset
        # pass, so classify their container format again using the final name.
        for export_filename, original_filename in asset_original_names.items():
            physical = source / export_filename.replace("/", os.sep)
            if physical.is_file():
                connection.execute(
                    "UPDATE assets SET detected_mime=? WHERE export_filename=?",
                    (detect_mime(physical, original_filename), export_filename),
                )

        graph_issues: Counter[str] = Counter()
        for shard_name in shard_names:
            shard_path = source / shard_name
            conversations = load_json(shard_path)
            if not isinstance(conversations, list):
                raise ValueError(f"Conversation shard is not a list: {shard_name}")
            for conversation in conversations:
                if not isinstance(conversation, dict):
                    continue
                conversation_id = str(conversation.get("id") or conversation.get("conversation_id") or "")
                if not conversation_id:
                    raise ValueError(f"Conversation without an id in {shard_name}")
                title = str(conversation.get("title") or "Untitled conversation")
                mapping = conversation.get("mapping")
                if not isinstance(mapping, dict):
                    mapping = {}
                lineage, has_cycle = current_path(mapping, conversation.get("current_node"))
                lineage_order = {node_id: index for index, node_id in enumerate(lineage)}
                if has_cycle:
                    graph_issues["cycles"] += 1
                if conversation.get("current_node") not in mapping:
                    graph_issues["missing_current_nodes"] += 1
                for mapping_key, node in mapping.items():
                    if isinstance(node, dict):
                        node_id = node.get("id")
                        if isinstance(node_id, str) and node_id != mapping_key:
                            graph_issues["mapping_key_node_id_mismatches"] += 1
                        parent = node.get("parent")
                        if isinstance(parent, str) and parent not in mapping:
                            graph_issues["missing_parents"] += 1

                conversation_metadata = {key: value for key, value in conversation.items() if key != "mapping"}
                message_count = sum(
                    1
                    for node in mapping.values()
                    if isinstance(node, dict) and isinstance(node.get("message"), dict)
                )
                current_message_count = sum(
                    1
                    for node_id in lineage
                    if isinstance(mapping.get(node_id), dict)
                    and isinstance(mapping[node_id].get("message"), dict)
                )
                connection.execute(
                    """
                    INSERT INTO conversations(
                        id, kind, title, create_time, update_time, current_node,
                        default_model_slug, is_archived, is_starred, is_do_not_remember,
                        source_file, message_count, current_path_message_count, metadata_json
                    ) VALUES (?, 'personal', ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        conversation_id,
                        title,
                        parse_time(conversation.get("create_time")),
                        parse_time(conversation.get("update_time")),
                        conversation.get("current_node"),
                        conversation.get("default_model_slug"),
                        as_bool_int(conversation.get("is_archived")),
                        as_bool_int(conversation.get("is_starred")),
                        as_bool_int(conversation.get("is_do_not_remember")),
                        shard_name,
                        message_count,
                        current_message_count,
                        compact_json(conversation_metadata),
                    ),
                )
                counters["personal_conversations"] += 1

                for source_order, (mapping_key, node) in enumerate(mapping.items()):
                    if not isinstance(node, dict) or not isinstance(node.get("message"), dict):
                        continue
                    message = node["message"]
                    author = message.get("author") if isinstance(message.get("author"), dict) else {}
                    content = message.get("content") if isinstance(message.get("content"), dict) else {}
                    metadata = message.get("metadata") if isinstance(message.get("metadata"), dict) else {}
                    role = author.get("role") if isinstance(author.get("role"), str) else None
                    content_type = content.get("content_type") if isinstance(content.get("content_type"), str) else None
                    node_id = str(node.get("id") or mapping_key)
                    insert_message(
                        connection,
                        fts_enabled=fts_enabled,
                        conversation_id=conversation_id,
                        title=title,
                        node_id=node_id,
                        message_id=str(message.get("id")) if message.get("id") is not None else None,
                        parent_node_id=node.get("parent") if isinstance(node.get("parent"), str) else None,
                        role=role,
                        author_name=author.get("name") if isinstance(author.get("name"), str) else None,
                        create_time=parse_time(message.get("create_time")),
                        content_type=content_type,
                        content=content,
                        metadata=metadata,
                        is_current_path=as_bool_int(node_id in lineage_order),
                        path_order=lineage_order.get(node_id),
                        source_order=source_order,
                        asset_names=asset_names,
                        asset_original_names=asset_original_names,
                    )
                    counters["personal_messages"] += 1
                    counters["current_path_messages"] += 1 if node_id in lineage_order else 0
                    roles[role or "unknown"] += 1
                    content_types[content_type or "unknown"] += 1

        group_path = source / "group_chats.json"
        group_data = load_json(group_path) if group_path.is_file() else {}
        group_chats = group_data.get("chats", []) if isinstance(group_data, dict) else []
        if not isinstance(group_chats, list):
            group_chats = []
        for chat_index, chat in enumerate(group_chats):
            if not isinstance(chat, dict):
                continue
            raw_id = str(chat.get("id") or chat_index)
            conversation_id = f"group:{raw_id}"
            title = str(chat.get("name") or chat.get("assistant_name") or "Group chat")
            messages = chat.get("messages") if isinstance(chat.get("messages"), list) else []
            chat_metadata = {key: value for key, value in chat.items() if key != "messages"}
            connection.execute(
                """
                INSERT INTO conversations(
                    id, kind, title, create_time, update_time, source_file,
                    message_count, current_path_message_count, metadata_json
                ) VALUES (?, 'group', ?, ?, ?, 'group_chats.json', ?, ?, ?)
                """,
                (
                    conversation_id,
                    title,
                    parse_time(chat.get("created_at")),
                    parse_time(chat.get("updated_at")),
                    len(messages),
                    len(messages),
                    compact_json(chat_metadata),
                ),
            )
            counters["group_conversations"] += 1
            for source_order, message in enumerate(messages):
                if not isinstance(message, dict):
                    continue
                message_id = str(message.get("id") or f"{raw_id}:{source_order}")
                content = {"content_type": "text", "parts": [message.get("text") or ""]}
                metadata = {
                    key: value
                    for key, value in message.items()
                    if key not in {"id", "role", "text", "created_at", "updated_at"}
                }
                role = message.get("role") if isinstance(message.get("role"), str) else None
                insert_message(
                    connection,
                    fts_enabled=fts_enabled,
                    conversation_id=conversation_id,
                    title=title,
                    node_id=message_id,
                    message_id=message_id,
                    parent_node_id=None,
                    role=role,
                    author_name=None,
                    create_time=parse_time(message.get("created_at")),
                    content_type="text",
                    content=content,
                    metadata=metadata,
                    is_current_path=1,
                    path_order=source_order,
                    source_order=source_order,
                    asset_names=asset_names,
                    asset_original_names=asset_original_names,
                )
                counters["group_messages"] += 1
                roles[role or "unknown"] += 1
                content_types["text"] += 1

        shared_path = source / "shared_conversations.json"
        shared_records = load_json(shared_path) if shared_path.is_file() else []
        if not isinstance(shared_records, list):
            shared_records = []
        for index, record in enumerate(shared_records):
            if not isinstance(record, dict):
                continue
            share_id = str(record.get("id") or f"share:{index}")
            conversation_id = record.get("conversation_id")
            connection.execute(
                "INSERT OR REPLACE INTO shared_conversations VALUES (?, ?, ?, ?, ?)",
                (
                    share_id,
                    conversation_id,
                    record.get("title"),
                    as_bool_int(record.get("is_anonymous")),
                    compact_json(record),
                ),
            )
            if isinstance(conversation_id, str):
                connection.execute(
                    "UPDATE conversations SET is_shared = 1 WHERE id = ?",
                    (conversation_id,),
                )
            counters["shared_records"] += 1

        build_digest = hashlib.sha256()
        build_digest.update(SCHEMA_VERSION.encode("ascii"))
        build_digest.update(INDEX_FORMAT_VERSION.encode("ascii"))
        build_digest.update(importer_digest.encode("ascii"))
        build_digest.update(f"hash_assets={as_bool_int(hash_assets)}".encode("ascii"))
        for digest in source_hashes:
            build_digest.update(digest.encode("ascii"))
        for digest in asset_hashes:
            build_digest.update(digest.encode("ascii"))
        build_id = build_digest.hexdigest()[:20]
        set_meta(connection, "schema_version", SCHEMA_VERSION)
        set_meta(connection, "index_format_version", INDEX_FORMAT_VERSION)
        set_meta(connection, "importer_sha256", importer_digest)
        set_meta(connection, "build_id", build_id)
        set_meta(connection, "imported_at", datetime.now(tz=timezone.utc).isoformat())
        set_meta(connection, "source_root", str(source.resolve()))
        set_meta(connection, "manifest_version", manifest.get("version"))
        set_meta(connection, "shards", shard_names)
        set_meta(connection, "fts5", as_bool_int(fts_enabled))
        set_meta(connection, "assets_hashed", as_bool_int(hash_assets))
        set_meta(connection, "counts", dict(counters))
        set_meta(connection, "content_types", dict(content_types))
        set_meta(connection, "roles", dict(roles))
        set_meta(connection, "graph_issues", dict(graph_issues))
        connection.commit()
        integrity = connection.execute("PRAGMA integrity_check").fetchone()[0]
        if integrity != "ok":
            raise RuntimeError(f"SQLite integrity check failed: {integrity}")
        return {
            "build_id": build_id,
            "fts5": fts_enabled,
            "counts": dict(counters),
            "content_types": dict(content_types),
            "roles": dict(roles),
            "graph_issues": dict(graph_issues),
        }
    finally:
        connection.close()


def read_meta(connection: sqlite3.Connection) -> dict[str, str]:
    return {row["key"]: row["value"] for row in connection.execute("SELECT key, value FROM archive_meta")}


def database_stats(connection: sqlite3.Connection, database_path: Path) -> dict[str, Any]:
    meta = read_meta(connection)
    result: dict[str, Any] = {
        "database": str(database_path.resolve()),
        "database_size_bytes": database_path.stat().st_size,
        "build_id": meta.get("build_id"),
        "schema_version": meta.get("schema_version"),
        "index_format_version": meta.get("index_format_version"),
        "imported_at": meta.get("imported_at"),
        "fts5": meta.get("fts5") == "1",
        "personal_conversations": connection.execute(
            "SELECT count(*) FROM conversations WHERE kind='personal'"
        ).fetchone()[0],
        "group_conversations": connection.execute(
            "SELECT count(*) FROM conversations WHERE kind='group'"
        ).fetchone()[0],
        "messages": connection.execute("SELECT count(*) FROM messages").fetchone()[0],
        "current_path_messages": connection.execute(
            "SELECT count(*) FROM messages WHERE is_current_path=1"
        ).fetchone()[0],
        "alternate_branch_messages": connection.execute(
            "SELECT count(*) FROM messages WHERE is_current_path=0"
        ).fetchone()[0],
        "assets": connection.execute("SELECT count(*) FROM assets").fetchone()[0],
        "assets_with_display_names": connection.execute(
            "SELECT count(*) FROM assets WHERE original_filename IS NOT NULL"
        ).fetchone()[0],
        "asset_bytes": connection.execute("SELECT coalesce(sum(size_bytes),0) FROM assets").fetchone()[0],
        "message_asset_references": connection.execute(
            "SELECT count(*) FROM message_assets"
        ).fetchone()[0],
        "resolved_message_asset_references": connection.execute(
            "SELECT count(*) FROM message_assets WHERE export_filename IS NOT NULL"
        ).fetchone()[0],
        "unresolved_message_asset_references": connection.execute(
            "SELECT count(*) FROM message_assets WHERE export_filename IS NULL"
        ).fetchone()[0],
        "library_records": connection.execute("SELECT count(*) FROM library_files").fetchone()[0],
        "library_records_with_conversation_links": connection.execute(
            """
            SELECT count(*) FROM library_files lf
            WHERE EXISTS (
                SELECT 1 FROM conversations c
                WHERE c.id = lf.initiating_conversation_id
                   OR c.id = lf.origination_thread_id
            )
            """
        ).fetchone()[0],
        "library_records_with_exported_assets": connection.execute(
            "SELECT count(*) FROM library_files WHERE export_filename IS NOT NULL"
        ).fetchone()[0],
        "shared_records": connection.execute("SELECT count(*) FROM shared_conversations").fetchone()[0],
    }
    try:
        imported_counts = json.loads(meta.get("counts", "{}"))
        result["conversation_asset_name_mappings"] = imported_counts.get("asset_mapped", 0)
        result["content_types"] = json.loads(meta.get("content_types", "{}"))
        result["roles"] = json.loads(meta.get("roles", "{}"))
    except json.JSONDecodeError:
        pass
    return result


def fts_expression(query: str) -> str:
    tokens = re.findall(r"\w+", query, flags=re.UNICODE)[:24]
    if not tokens:
        raise ValueError("Search query contains no searchable words")
    return " AND ".join(f'"{token.replace(chr(34), chr(34) * 2)}"*' for token in tokens)


def search_messages(
    connection: sqlite3.Connection,
    query: str,
    limit: int,
    all_branches: bool,
    include_reasoning: bool,
    all_roles: bool,
) -> list[dict[str, Any]]:
    meta = read_meta(connection)
    filters: list[str] = []
    parameters: list[Any] = []
    if not all_branches:
        filters.append("m.is_current_path = 1")
    if not include_reasoning:
        filters.append("coalesce(m.content_type, '') NOT IN ('thoughts', 'reasoning_recap')")
    if not all_roles:
        filters.append("m.role IN ('user', 'assistant')")
    where_suffix = " AND " + " AND ".join(filters) if filters else ""

    if meta.get("fts5") == "1":
        sql = f"""
            SELECT c.id AS conversation_id, c.title, c.kind, m.node_id, m.message_id,
                   m.role, m.content_type, m.create_time, m.is_current_path,
                   snippet(message_fts, 1, '[', ']', ' … ', 28) AS snippet,
                   bm25(message_fts, 8.0, 1.0, 4.0) AS rank
            FROM message_fts
            JOIN messages m ON m.row_id = message_fts.rowid
            JOIN conversations c ON c.id = m.conversation_id
            WHERE message_fts MATCH ?{where_suffix}
            ORDER BY rank, m.is_current_path DESC, m.create_time DESC
            LIMIT ?
        """
        parameters = [fts_expression(query), limit]
    else:
        tokens = [token.casefold() for token in re.findall(r"\w+", query, flags=re.UNICODE)[:24]]
        if not tokens:
            raise ValueError("Search query contains no searchable words")
        token_filters = []
        for token in tokens:
            token_filters.append(
                "instr(casefold(c.title || ' ' || m.text), ?) > 0"
            )
            parameters.append(token)
        sql = f"""
            SELECT c.id AS conversation_id, c.title, c.kind, m.node_id, m.message_id,
                   m.role, m.content_type, m.create_time, m.is_current_path,
                   substr(replace(m.text, char(10), ' '), 1, 500) AS snippet,
                   0.0 AS rank
            FROM messages m
            JOIN conversations c ON c.id = m.conversation_id
            WHERE {' AND '.join(token_filters)}{where_suffix}
            ORDER BY m.is_current_path DESC, m.create_time DESC
            LIMIT ?
        """
        parameters.append(limit)
    return [dict(row) for row in connection.execute(sql, parameters)]


def print_search_results(results: list[dict[str, Any]], as_json: bool) -> None:
    if as_json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
        return
    if not results:
        print("No matching messages found.")
        return
    for index, result in enumerate(results, 1):
        branch = "current" if result["is_current_path"] else "alternate"
        snippet = " ".join((result.get("snippet") or "").split())
        print(
            f"{index}. {result['title']} | {result['kind']} | {result.get('role') or 'unknown'} "
            f"| {iso_time(result.get('create_time'))} | {branch}"
        )
        print(f"   conversation_id={result['conversation_id']} node_id={result['node_id']}")
        print(f"   {snippet}")


def resolve_conversation(connection: sqlite3.Connection, selector: str) -> sqlite3.Row | None:
    exact = connection.execute("SELECT * FROM conversations WHERE id = ?", (selector,)).fetchone()
    if exact:
        return exact
    matches = connection.execute(
        """
        SELECT * FROM conversations
        WHERE id LIKE ? OR instr(casefold(title), casefold(?)) > 0
        ORDER BY update_time DESC
        LIMIT 11
        """,
        (f"{selector}%", selector),
    ).fetchall()
    if len(matches) == 1:
        return matches[0]
    if len(matches) > 1:
        print("Conversation selector is ambiguous. Candidates:", file=sys.stderr)
        for row in matches[:10]:
            print(f"- {row['id']} | {row['title']}", file=sys.stderr)
    return None


def conversation_asset_rows(
    connection: sqlite3.Connection, conversation_id: str, limit: int | None = None
) -> list[dict[str, Any]]:
    rows = [
        dict(row)
        for row in connection.execute(
            """
        SELECT ma.message_row_id, ma.reference, m.node_id, m.create_time,
               a.export_filename, a.original_filename, a.source_path,
               a.size_bytes, a.detected_mime, a.sha256
        FROM message_assets ma
        JOIN messages m ON m.row_id = ma.message_row_id
        LEFT JOIN assets a ON a.export_filename = ma.export_filename
        WHERE m.conversation_id = ?
        ORDER BY coalesce(m.path_order, 2147483647), m.source_order,
                 coalesce(a.original_filename, ma.reference)
        """,
            (conversation_id,),
        )
    ]

    # Older library entries are linked to a thread without appearing as a
    # structured attachment pointer in that thread's exported messages.
    library_rows = connection.execute(
        """
        SELECT NULL AS message_row_id,
               coalesce(lf.file_id, lf.record_id) AS reference,
               lf.origination_message_id AS node_id,
               NULL AS create_time,
               a.export_filename, a.original_filename, a.source_path,
               a.size_bytes, a.detected_mime, a.sha256
        FROM library_files lf
        LEFT JOIN assets a ON a.export_filename = lf.export_filename
        WHERE lf.initiating_conversation_id = ? OR lf.origination_thread_id = ?
        ORDER BY coalesce(a.original_filename, lf.file_name, lf.record_id)
        """,
        (conversation_id, conversation_id),
    ).fetchall()
    seen_assets = {row.get("export_filename") or row["reference"] for row in rows}
    for library_row in library_rows:
        candidate = dict(library_row)
        key = candidate.get("export_filename") or candidate["reference"]
        if key not in seen_assets:
            rows.append(candidate)
            seen_assets.add(key)
    return rows[:limit] if limit is not None else rows


def command_import(args: argparse.Namespace) -> int:
    source = Path(args.source).expanduser().resolve()
    database_path = Path(args.db).expanduser().resolve()
    if not source.is_dir():
        print(f"Source directory does not exist: {source}", file=sys.stderr)
        return 2
    database_path.parent.mkdir(parents=True, exist_ok=True)
    if database_path.exists() and not args.replace:
        print(
            f"Database already exists: {database_path}\nUse --replace to rebuild it explicitly.",
            file=sys.stderr,
        )
        return 2
    temporary = database_path.with_name(f"{database_path.name}.building")
    if temporary.exists():
        temporary.unlink()
    try:
        build_database(source, temporary, args.hash_assets)
        verification = verify_database(temporary, source)
        if not verification["ok"]:
            reasons = "; ".join(verification["failures"])
            raise RuntimeError(f"New index did not pass verification: {reasons}")
        if database_path.exists() and args.keep_backup:
            backup_stamp = datetime.now(tz=timezone.utc).strftime("%Y%m%dT%H%M%SZ")
            backup = database_path.with_name(f"index.backup-{backup_stamp}.sqlite3")
            os.replace(database_path, backup)
        os.replace(temporary, database_path)
    except Exception as exc:
        if temporary.exists():
            temporary.unlink()
        print(f"Import failed: {exc}", file=sys.stderr)
        return 1
    with closing(connect_database(database_path)) as connection:
        stats = database_stats(connection, database_path)
    print(json.dumps(stats, ensure_ascii=False, indent=2))
    print(json.dumps(verification, ensure_ascii=False, indent=2))
    return 0


def command_search(args: argparse.Namespace) -> int:
    database_path = Path(args.db).expanduser().resolve()
    if not database_path.is_file():
        print(f"Private chat index not found: {database_path}", file=sys.stderr)
        return 2
    try:
        with closing(connect_database(database_path)) as connection:
            results = search_messages(
                connection,
                args.query,
                args.limit,
                args.all_branches,
                args.include_reasoning,
                args.all_roles,
            )
    except (ValueError, sqlite3.Error) as exc:
        print(f"Search failed: {exc}", file=sys.stderr)
        return 1
    print_search_results(results, args.json)
    return 0


def command_show(args: argparse.Namespace) -> int:
    database_path = Path(args.db).expanduser().resolve()
    if not database_path.is_file():
        print(f"Private chat index not found: {database_path}", file=sys.stderr)
        return 2
    with closing(connect_database(database_path)) as connection:
        conversation = resolve_conversation(connection, args.conversation)
        if conversation is None:
            return 2
        filters = ["m.conversation_id = ?"]
        parameters: list[Any] = [conversation["id"]]
        if not args.all_branches:
            filters.append("m.is_current_path = 1")
        if not args.include_reasoning:
            filters.append("coalesce(m.content_type, '') NOT IN ('thoughts', 'reasoning_recap')")
        if not args.all_roles:
            filters.append("m.role IN ('user', 'assistant')")
        rows = connection.execute(
            f"""
            SELECT m.* FROM messages m
            WHERE {' AND '.join(filters)}
            ORDER BY coalesce(m.path_order, 2147483647),
                     coalesce(m.create_time, 0), m.source_order
            """,
            parameters,
        ).fetchall()
        attachments = conversation_asset_rows(connection, conversation["id"])

    attachments_by_message: dict[int, list[dict[str, Any]]] = {}
    for attachment in attachments:
        attachments_by_message.setdefault(attachment["message_row_id"], []).append(attachment)

    if args.json:
        messages_payload: list[dict[str, Any]] = []
        for row in rows:
            message_payload = dict(row)
            message_payload["attachments"] = attachments_by_message.get(row["row_id"], [])
            messages_payload.append(message_payload)
        payload = {
            "conversation": dict(conversation),
            "messages": messages_payload,
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0

    print(f"# {conversation['title']}")
    print(f"conversation_id={conversation['id']} kind={conversation['kind']} messages={len(rows)}")
    for row in rows:
        text = row["text"] or ""
        if not args.full and len(text) > args.max_chars:
            text = text[: args.max_chars] + "\n[message truncated; use --full to inspect all text]"
        branch = "current" if row["is_current_path"] else "alternate"
        print(
            f"\n## {row['role'] or 'unknown'} | {iso_time(row['create_time'])} "
            f"| {row['content_type'] or 'unknown'} | {branch} | node={row['node_id']}"
        )
        print(text)
        for attachment in attachments_by_message.get(row["row_id"], []):
            label = attachment.get("original_filename") or attachment["reference"]
            target = attachment.get("source_path") or "unresolved export reference"
            print(f"[attachment] {label} -> {target}")
    return 0


def command_assets(args: argparse.Namespace) -> int:
    database_path = Path(args.db).expanduser().resolve()
    if not database_path.is_file():
        print(f"Private chat index not found: {database_path}", file=sys.stderr)
        return 2
    with closing(connect_database(database_path)) as connection:
        if args.conversation:
            conversation = resolve_conversation(connection, args.conversation)
            if conversation is None:
                return 2
            rows = conversation_asset_rows(connection, conversation["id"], args.limit)
        elif args.query:
            rows = [
                dict(row)
                for row in connection.execute(
                    """
                    SELECT NULL AS message_row_id, export_filename AS reference,
                           NULL AS node_id, NULL AS create_time,
                           export_filename, original_filename, source_path,
                           size_bytes, detected_mime, sha256
                    FROM assets
                    WHERE instr(
                        casefold(coalesce(original_filename, '') || ' ' || export_filename),
                        casefold(?)
                    ) > 0
                    ORDER BY coalesce(original_filename, export_filename)
                    LIMIT ?
                    """,
                    (args.query, args.limit),
                )
            ]
        else:
            print("Provide an asset query or --conversation.", file=sys.stderr)
            return 2

    if args.json:
        print(json.dumps(rows, ensure_ascii=False, indent=2))
        return 0
    if not rows:
        print("No matching attachment records found.")
        return 0
    for index, row in enumerate(rows, 1):
        label = row.get("original_filename") or row["reference"]
        status = row.get("detected_mime") or "unresolved"
        size = row.get("size_bytes")
        size_text = f"{size} bytes" if size is not None else "unknown size"
        print(f"{index}. {label} | {status} | {size_text}")
        if row.get("node_id"):
            print(f"   node_id={row['node_id']} reference={row['reference']}")
        print(f"   {row.get('source_path') or 'No matching exported binary file'}")
    return 0


def command_stats(args: argparse.Namespace) -> int:
    database_path = Path(args.db).expanduser().resolve()
    if not database_path.is_file():
        print(f"Private chat index not found: {database_path}", file=sys.stderr)
        return 2
    with closing(connect_database(database_path)) as connection:
        stats = database_stats(connection, database_path)
    print(json.dumps(stats, ensure_ascii=False, indent=2))
    return 0


def verify_database(database_path: Path, source: Path | None = None) -> dict[str, Any]:
    checks: dict[str, Any] = {}
    failures: list[str] = []
    with closing(connect_database(database_path)) as connection:
        checks["integrity_check"] = connection.execute("PRAGMA integrity_check").fetchone()[0]
        if checks["integrity_check"] != "ok":
            failures.append("SQLite integrity check failed")
        foreign_keys = connection.execute("PRAGMA foreign_key_check").fetchall()
        checks["foreign_key_violations"] = len(foreign_keys)
        if foreign_keys:
            failures.append("Foreign-key violations found")
        meta = read_meta(connection)
        checks["schema_version"] = meta.get("schema_version")
        checks["index_format_version"] = meta.get("index_format_version")
        if meta.get("schema_version") != SCHEMA_VERSION:
            failures.append("Database schema version does not match the importer")
        if meta.get("index_format_version") != INDEX_FORMAT_VERSION:
            failures.append("Database index format does not match the importer")
        message_count = connection.execute("SELECT count(*) FROM messages").fetchone()[0]
        conversation_message_total = connection.execute(
            "SELECT coalesce(sum(message_count), 0) FROM conversations"
        ).fetchone()[0]
        checks["messages"] = message_count
        checks["conversation_message_total"] = conversation_message_total
        if message_count != conversation_message_total:
            failures.append("Message totals do not match conversation metadata")
        current_path_rows = connection.execute(
            "SELECT count(*) FROM messages WHERE is_current_path=1"
        ).fetchone()[0]
        conversation_current_path_total = connection.execute(
            "SELECT coalesce(sum(current_path_message_count), 0) FROM conversations"
        ).fetchone()[0]
        checks["current_path_messages"] = current_path_rows
        checks["conversation_current_path_total"] = conversation_current_path_total
        if current_path_rows != conversation_current_path_total:
            failures.append("Current-path totals do not match conversation metadata")
        if meta.get("fts5") == "1":
            fts_count = connection.execute("SELECT count(*) FROM message_fts").fetchone()[0]
            checks["fts_rows"] = fts_count
            if fts_count != message_count:
                failures.append("FTS row count does not match message count")
            try:
                connection.execute(
                    "INSERT INTO message_fts(message_fts) VALUES ('integrity-check')"
                )
                checks["fts_integrity_check"] = "ok"
            except sqlite3.DatabaseError as exc:
                if "readonly" in str(exc).casefold() or "read-only" in str(exc).casefold():
                    checks["fts_integrity_check"] = "skipped: database is read-only"
                else:
                    checks["fts_integrity_check"] = str(exc)
                    failures.append("FTS internal integrity check failed")
            fts_missing_rows = connection.execute(
                """
                SELECT count(*)
                FROM messages m
                LEFT JOIN message_fts ON message_fts.rowid = m.row_id
                WHERE message_fts.rowid IS NULL
                """
            ).fetchone()[0]
            fts_orphan_rows = connection.execute(
                """
                SELECT count(*)
                FROM message_fts
                LEFT JOIN messages m ON m.row_id = message_fts.rowid
                WHERE m.row_id IS NULL
                """
            ).fetchone()[0]
            checks["fts_missing_rows"] = fts_missing_rows
            checks["fts_orphan_rows"] = fts_orphan_rows
            if fts_missing_rows or fts_orphan_rows:
                failures.append("FTS row ids do not match normalized messages")
            fts_content_mismatches = connection.execute(
                """
                SELECT count(*)
                FROM message_fts
                JOIN messages m ON m.row_id = message_fts.rowid
                JOIN conversations c ON c.id = m.conversation_id
                WHERE message_fts.title IS NOT c.title
                   OR message_fts.text IS NOT m.text
                   OR message_fts.conversation_id IS NOT m.conversation_id
                   OR message_fts.role IS NOT m.role
                """
            ).fetchone()[0]
            checks["fts_content_mismatches"] = fts_content_mismatches
            if fts_content_mismatches:
                failures.append("FTS content does not match normalized messages")
        checks["missing_manifest_files"] = connection.execute(
            "SELECT count(*) FROM archive_files WHERE exists_flag=0"
        ).fetchone()[0]
        checks["manifest_size_mismatches"] = connection.execute(
            "SELECT count(*) FROM archive_files WHERE size_matches=0"
        ).fetchone()[0]
        # The manifest's own sites/export_manifest.json entry is a documented
        # self-reference placeholder; all other mismatches are failures.
        substantive_mismatches = connection.execute(
            """
            SELECT count(*) FROM archive_files
            WHERE size_matches=0 AND path <> 'sites/export_manifest.json'
            """
        ).fetchone()[0]
        if checks["missing_manifest_files"]:
            failures.append("Manifest-listed files are missing")
        if substantive_mismatches:
            failures.append("Manifest-listed file sizes do not match")
        checks["missing_assets"] = connection.execute(
            "SELECT count(*) FROM assets WHERE exists_flag=0"
        ).fetchone()[0]
        if checks["missing_assets"]:
            failures.append("Asset files are missing")
        invalid_library_ids = connection.execute(
            "SELECT count(*) FROM library_files WHERE trim(record_id)='' OR record_id LIKE '{%'"
        ).fetchone()[0]
        checks["invalid_library_record_ids"] = invalid_library_ids
        if invalid_library_ids:
            failures.append("Library record identifiers were not normalized")
        checks["library_conversation_links"] = connection.execute(
            """
            SELECT count(*) FROM library_files lf
            WHERE EXISTS (
                SELECT 1 FROM conversations c
                WHERE c.id = lf.initiating_conversation_id
                   OR c.id = lf.origination_thread_id
            )
            """
        ).fetchone()[0]
        try:
            graph_issues = json.loads(meta.get("graph_issues", "{}"))
        except json.JSONDecodeError:
            graph_issues = {"invalid_metadata": 1}
        checks["graph_issues"] = graph_issues
        if any(graph_issues.values()):
            failures.append("Conversation graph issues were detected")

        if source is not None:
            source = source.expanduser().resolve()
            input_mismatches = 0
            for row in connection.execute("SELECT * FROM source_inputs"):
                physical = source / row["path"].replace("/", os.sep)
                if (
                    not physical.is_file()
                    or physical.stat().st_size != row["size_bytes"]
                    or file_sha256(physical) != row["sha256"]
                ):
                    input_mismatches += 1
            checks["source_input_mismatches"] = input_mismatches
            if input_mismatches:
                failures.append("Source JSON inputs changed after import")

            archive_file_mismatches = 0
            for row in connection.execute("SELECT * FROM archive_files"):
                physical = source / row["path"].replace("/", os.sep)
                if not physical.is_file():
                    archive_file_mismatches += 1
                    continue
                expected = row["expected_size_bytes"]
                if (
                    expected is not None
                    and physical.stat().st_size != expected
                    and row["path"] != "sites/export_manifest.json"
                ):
                    archive_file_mismatches += 1
            checks["source_archive_file_mismatches"] = archive_file_mismatches
            if archive_file_mismatches:
                failures.append("Manifest-listed source files changed after import")

            asset_size_mismatches = 0
            asset_hash_mismatches = 0
            hashed_assets_checked = 0
            for row in connection.execute(
                "SELECT export_filename, size_bytes, sha256 FROM assets"
            ):
                physical = source / row["export_filename"].replace("/", os.sep)
                if not physical.is_file() or physical.stat().st_size != row["size_bytes"]:
                    asset_size_mismatches += 1
                    continue
                if row["sha256"]:
                    hashed_assets_checked += 1
                    if file_sha256(physical) != row["sha256"]:
                        asset_hash_mismatches += 1
            checks["source_asset_size_mismatches"] = asset_size_mismatches
            checks["source_asset_hash_mismatches"] = asset_hash_mismatches
            checks["source_hashed_assets_checked"] = hashed_assets_checked
            if asset_size_mismatches:
                failures.append("Source asset files are missing or have changed size")
            if asset_hash_mismatches:
                failures.append("Source asset hashes changed after import")

        smoke = connection.execute(
            """
            SELECT row_id, text FROM messages
            WHERE is_current_path=1 AND role IN ('user','assistant')
              AND content_type IN ('text','multimodal_text') AND length(text) > 30
            ORDER BY row_id LIMIT 1
            """
        ).fetchone()
        smoke_ok = False
        if smoke and meta.get("fts5") == "1":
            token_match = re.search(r"\w{6,}", smoke["text"], flags=re.UNICODE)
            if token_match:
                expression = f'"{token_match.group(0)}"'
                smoke_ok = bool(
                    connection.execute(
                        "SELECT 1 FROM message_fts WHERE rowid=? AND message_fts MATCH ?",
                        (smoke["row_id"], expression),
                    ).fetchone()
                )
        elif smoke:
            smoke_ok = True
        checks["private_search_smoke_test"] = smoke_ok
        if not smoke_ok:
            failures.append("Private search smoke test failed")

    return {"ok": not failures, "checks": checks, "failures": failures}


def command_verify(args: argparse.Namespace) -> int:
    database_path = Path(args.db).expanduser().resolve()
    if not database_path.is_file():
        print(f"Private chat index not found: {database_path}", file=sys.stderr)
        return 2
    source = Path(args.source) if args.source else None
    result = verify_database(database_path, source)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["ok"] else 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Import and query a private local ChatGPT conversation archive."
    )
    parser.set_defaults(handler=None)
    subparsers = parser.add_subparsers(dest="command")

    import_parser = subparsers.add_parser("import", help="Build a private SQLite index")
    import_parser.add_argument("--source", required=True, help="ChatGPT export directory")
    import_parser.add_argument("--db", default=str(DEFAULT_DB), help="Output SQLite database")
    import_parser.add_argument("--replace", action="store_true", help="Rebuild an existing index")
    import_parser.add_argument(
        "--keep-backup",
        action="store_true",
        help="Keep the previous database when used together with --replace",
    )
    import_parser.add_argument(
        "--hash-assets",
        action="store_true",
        help="Also hash every binary asset (slower, strongest verification)",
    )
    import_parser.set_defaults(handler=command_import)

    search_parser = subparsers.add_parser("search", help="Search messages")
    search_parser.add_argument("query")
    search_parser.add_argument("--db", default=str(DEFAULT_DB))
    search_parser.add_argument("--limit", type=int, default=10)
    search_parser.add_argument("--all-branches", action="store_true")
    search_parser.add_argument("--include-reasoning", action="store_true")
    search_parser.add_argument("--all-roles", action="store_true")
    search_parser.add_argument("--json", action="store_true")
    search_parser.set_defaults(handler=command_search)

    show_parser = subparsers.add_parser("show", help="Show one conversation")
    show_parser.add_argument("conversation", help="Conversation id, id prefix, or unique title text")
    show_parser.add_argument("--db", default=str(DEFAULT_DB))
    show_parser.add_argument("--all-branches", action="store_true")
    show_parser.add_argument("--include-reasoning", action="store_true")
    show_parser.add_argument("--all-roles", action="store_true")
    show_parser.add_argument("--max-chars", type=int, default=6000)
    show_parser.add_argument("--full", action="store_true")
    show_parser.add_argument("--json", action="store_true")
    show_parser.set_defaults(handler=command_show)

    assets_parser = subparsers.add_parser("assets", help="Find exported attachment records")
    assets_parser.add_argument("query", nargs="?", help="Original or exported filename text")
    assets_parser.add_argument("--conversation", help="Conversation id, prefix, or unique title text")
    assets_parser.add_argument("--db", default=str(DEFAULT_DB))
    assets_parser.add_argument("--limit", type=int, default=50)
    assets_parser.add_argument("--json", action="store_true")
    assets_parser.set_defaults(handler=command_assets)

    stats_parser = subparsers.add_parser("stats", help="Show index statistics")
    stats_parser.add_argument("--db", default=str(DEFAULT_DB))
    stats_parser.set_defaults(handler=command_stats)

    verify_parser = subparsers.add_parser("verify", help="Verify index integrity")
    verify_parser.add_argument("--db", default=str(DEFAULT_DB))
    verify_parser.add_argument("--source", help="Also verify source JSON hashes")
    verify_parser.add_argument("--json", action="store_true")
    verify_parser.set_defaults(handler=command_verify)
    return parser


def main(argv: Iterable[str] | None = None) -> int:
    # Codex captures subprocess output as UTF-8; force that encoding on Windows
    # so Turkish titles and snippets remain readable regardless of console locale.
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if callable(reconfigure):
            reconfigure(encoding="utf-8", errors="replace")
    parser = build_parser()
    args = parser.parse_args(list(argv) if argv is not None else None)
    if args.handler is None:
        parser.print_help()
        return 2
    if hasattr(args, "limit") and not 1 <= args.limit <= 100:
        parser.error("--limit must be between 1 and 100")
    return int(args.handler(args))


if __name__ == "__main__":
    raise SystemExit(main())
