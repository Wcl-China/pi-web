"""Generate deterministic Jiyun Web PWA and favicon assets."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
ICON_DIR = ROOT / "public" / "icons"
FONT_PATH = Path(r"C:\Windows\Fonts\seguisb.ttf")


def create_icon(size: int) -> Image.Image:
    scale = size / 512

    def box(values: tuple[int, int, int, int]) -> tuple[int, int, int, int]:
        return tuple(round(value * scale) for value in values)

    image = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle(box((24, 24, 488, 488)), radius=round(116 * scale), fill="#12343a")

    # Compact cloud silhouette; generous margins keep it legible at favicon sizes.
    draw.ellipse(box((92, 194, 246, 348)), fill="white")
    draw.ellipse(box((164, 116, 346, 322)), fill="white")
    draw.ellipse(box((278, 176, 430, 348)), fill="white")
    draw.rounded_rectangle(box((110, 226, 414, 372)), radius=round(58 * scale), fill="white")

    font = ImageFont.truetype(str(FONT_PATH), round(190 * scale))
    text = "J"
    text_box = draw.textbbox((0, 0), text, font=font)
    text_width = text_box[2] - text_box[0]
    text_height = text_box[3] - text_box[1]
    draw.text(
        ((size - text_width) / 2, round(218 * scale) - text_height / 2 - text_box[1]),
        text,
        font=font,
        fill="#5f9f98",
    )
    return image


def main() -> None:
    ICON_DIR.mkdir(parents=True, exist_ok=True)
    for size, name in ((512, "icon-512.png"), (192, "icon-192.png"), (180, "apple-touch-icon.png")):
        create_icon(size).save(ICON_DIR / name, optimize=True)

    favicon = create_icon(256)
    favicon.save(ROOT / "app" / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)])


if __name__ == "__main__":
    main()
