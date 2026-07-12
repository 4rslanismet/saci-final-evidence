from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


WIDTH, HEIGHT = 1800, 840
REGULAR = Path(r"C:\Windows\Fonts\times.ttf")
BOLD = Path(r"C:\Windows\Fonts\timesbd.ttf")


def centered_multiline(draw: ImageDraw.ImageDraw, box, text, font, fill="#111827", spacing=7):
    left, top, right, bottom = box
    bbox = draw.multiline_textbbox((0, 0), text, font=font, align="center", spacing=spacing)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    x = left + (right - left - text_w) / 2
    y = top + (bottom - top - text_h) / 2
    draw.multiline_text((x, y), text, font=font, fill=fill, align="center", spacing=spacing)


def draw_box(draw, box, heading, body, fill):
    draw.rounded_rectangle(box, radius=22, fill=fill, outline="#334155", width=4)
    left, top, right, bottom = box
    heading_font = ImageFont.truetype(str(BOLD), 31)
    body_font = ImageFont.truetype(str(REGULAR), 25)
    centered_multiline(draw, (left + 20, top + 18, right - 20, top + 78), heading, heading_font)
    centered_multiline(draw, (left + 20, top + 75, right - 20, bottom - 18), body, body_font, fill="#334155")


def arrow(draw, start, end):
    draw.line([start, end], fill="#475569", width=6)
    x, y = end
    draw.polygon([(x, y), (x - 20, y - 12), (x - 20, y + 12)], fill="#475569")


def build(language: str, output: Path) -> None:
    image = Image.new("RGB", (WIDTH, HEIGHT), "white")
    draw = ImageDraw.Draw(image)
    title_font = ImageFont.truetype(str(BOLD), 42)

    if language == "tr":
        title = "SACI kanıt işleme hattı"
        boxes = [
            ("Kapsam ve beklenti", "6 varlık · 12 log çifti\n27 kontrol · 13 teknik"),
            ("Gözlenen kanıt", "Wazuh · Sysmon · pfSense\nMISP · Windows · Linux"),
            ("Tiplenmiş kanıt grafı", "Varlık · kaynak · kontrol · kural\nATT&CK · CTI · metrik\n97 beyan edilmiş düğüm · 171 kenar satırı"),
            ("SACI skorlama", "CWLC · CAC · MDC · CTIC · TF\naktif-ağırlık normalizasyonu"),
            ("Denetlenebilir çıktılar", "Skorlar · bütünlük bulguları\n17 artefakt · GitHub Pages"),
        ]
    else:
        title = "SACI evidence-processing pipeline"
        boxes = [
            ("Scope and expectations", "6 assets · 12 log pairs\n27 controls · 13 techniques"),
            ("Observed evidence", "Wazuh · Sysmon · pfSense\nMISP · Windows · Linux"),
            ("Typed evidence graph", "Assets · sources · controls · rules\nATT&CK · CTI · metrics\n97 declared nodes · 171 edge rows"),
            ("SACI scoring", "CWLC · CAC · MDC · CTIC · TF\nactive-weight normalization"),
            ("Auditable outputs", "Scores · integrity findings\n17 artifacts · GitHub Pages"),
        ]

    title_box = draw.textbbox((0, 0), title, font=title_font)
    draw.text(((WIDTH - (title_box[2] - title_box[0])) / 2, 35), title, font=title_font, fill="#0f172a")

    left_top = (55, 150, 500, 350)
    left_bottom = (55, 485, 500, 685)
    middle = (620, 230, 1190, 610)
    right_top = (1310, 150, 1745, 350)
    right_bottom = (1310, 485, 1745, 685)

    draw_box(draw, left_top, *boxes[0], "#eef4fb")
    draw_box(draw, left_bottom, *boxes[1], "#f8fafc")
    draw_box(draw, middle, *boxes[2], "#e8f1f8")
    draw_box(draw, right_top, *boxes[3], "#eef7f0")
    draw_box(draw, right_bottom, *boxes[4], "#fff8e8")

    arrow(draw, (500, 250), (620, 330))
    arrow(draw, (500, 585), (620, 510))
    arrow(draw, (1190, 330), (1310, 250))
    arrow(draw, (1190, 510), (1310, 585))

    output.parent.mkdir(parents=True, exist_ok=True)
    image.save(output, dpi=(300, 300), optimize=True)
    print(output)


if __name__ == "__main__":
    root = Path(__file__).resolve().parent
    build("tr", root / "pipeline_tr.png")
    build("en", root / "pipeline_en.png")
