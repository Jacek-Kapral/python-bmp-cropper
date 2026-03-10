"""
Skrypt do batchowego przycinania BMP do tego samego prostokąta (np. z zaznaczenia IrfanView).
Zapisuje wyniki jako 001.bmp, 002.bmp, ... w katalogu wyjściowym.
"""

from pathlib import Path

try:
    from PIL import Image
except ImportError:
    raise ImportError("Wymagana biblioteka Pillow: pip install Pillow")


# Parametry z IrfanView "Selection: 91, 2; 218x217"
CROP_LEFT = 91
CROP_TOP = 2
CROP_WIDTH = 218
CROP_HEIGHT = 217


def crop_bmp_series(
    source_dir: str | Path,
    output_dir: str | Path | None = None,
    *,
    left: int = CROP_LEFT,
    top: int = CROP_TOP,
    width: int = CROP_WIDTH,
    height: int = CROP_HEIGHT,
) -> list[Path]:
    """
    Przechodzi przez wszystkie pliki .bmp w source_dir, wycina z każdego
    prostokąt (left, top, width, height) i zapisuje jako 001.bmp, 002.bmp, ...
    w output_dir (domyślnie podkatalog 'cropped' w source_dir).

    @param source_dir Katalog z plikami BMP
    @param output_dir Katalog wynikowy (None = source_dir/cropped)
    @param left Lewy brzeg wycinanego obszaru (px)
    @param top Górny brzeg wycinanego obszaru (px)
    @param width Szerokość wycinka (px)
    @param height Wysokość wycinka (px)
    @returns Lista ścieżek do zapisanych plików
    """
    source_dir = Path(source_dir)
    output_dir = Path(output_dir) if output_dir else source_dir / "cropped"
    output_dir.mkdir(parents=True, exist_ok=True)

    bmp_files = sorted(source_dir.glob("*.bmp"))
    if not bmp_files:
        raise FileNotFoundError(f"Brak plików .bmp w: {source_dir}")

    saved: list[Path] = []
    for i, src_path in enumerate(bmp_files, start=1):
        out_name = f"{i:03d}.bmp"
        out_path = output_dir / out_name
        with Image.open(src_path) as img:
            cropped = img.crop((left, top, left + width, top + height))
            cropped.save(out_path, format="BMP")
        saved.append(out_path)
    return saved


if __name__ == "__main__":
    import sys

    src = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    out = Path(sys.argv[2]) if len(sys.argv) > 2 else None
    crop_bmp_series(src, out)
