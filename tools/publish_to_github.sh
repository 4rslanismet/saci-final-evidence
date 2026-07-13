#!/usr/bin/env bash
set -euo pipefail
REPO_URL="${1:-}"
if [ -z "$REPO_URL" ]; then
  echo "Usage: ./publish_to_github.sh https://github.com/<user>/<repo>.git"
  exit 1
fi

# Refuse to publish a ChatGPT export accidentally copied into the site tree.
PRIVATE_EXPORTS="$(
  find . -type f \
    ! -path './.git/*' \
    ! -path './.private/*' \
    \( -name 'chat.html' \
       -o -name 'conversations.json' \
       -o -name 'conversations-*.json' \
       -o -name 'conversation_asset_file_names.json' \
       -o -name 'export_manifest.json' \
       -o -name 'group_chats.json' \
       -o -name 'library_files.json' \
       -o -name 'shared_conversations.json' \
       -o -name 'user.json' \
       -o -name 'user_settings.json' \
       -o -name 'file-*.dat' \
       -o -name 'file_*.dat' \) \
    -print
)"
if [ -n "$PRIVATE_EXPORTS" ]; then
  echo "Refusing to publish: private ChatGPT export files were found:" >&2
  echo "$PRIVATE_EXPORTS" >&2
  exit 1
fi

git init

# Ignore rules cannot protect a private file that was already tracked earlier.
TRACKED_PRIVATE="$(git ls-files -- .private)"
if [ -n "$TRACKED_PRIVATE" ]; then
  echo "Refusing to publish: files under .private are already tracked by Git:" >&2
  echo "$TRACKED_PRIVATE" >&2
  exit 1
fi

# Deleted/ignored files can still leak through earlier commits in main history.
if git rev-parse --verify HEAD >/dev/null 2>&1; then
  HISTORICAL_PRIVATE="$(
    git log --all --name-only --pretty=format: \
      | grep -E '(^|/)\.private(/|$)|(^|/)(chat\.html|conversations(-[0-9]+)?\.json|conversation_asset_file_names\.json|export_manifest\.json|group_chats\.json|library_files\.json|shared_conversations\.json|user\.json|user_settings\.json|file[-_].*\.dat)$' \
      || true
  )"
  if [ -n "$HISTORICAL_PRIVATE" ]; then
    echo "Refusing to publish: private ChatGPT export paths exist in Git history:" >&2
    echo "$HISTORICAL_PRIVATE" >&2
    exit 1
  fi
fi

git branch -M main
git add .
git commit -m "Publish SACI final evidence viewer"
git remote add origin "$REPO_URL"
git push -u origin main
