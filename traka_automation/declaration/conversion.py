import subprocess
from pathlib import Path

from PIL import Image

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".tiff"}
OFFICE_DOCUMENT_EXTENSIONS = {".xlsx", ".docx"}


def convert_office_document_to_pdf(file_path: Path, output_dir: Path) -> Path:
    """Convert an office document to PDF with LibreOffice."""
    result = subprocess.run(
        [
            "libreoffice",
            "--headless",
            "--convert-to",
            "pdf",
            "--outdir",
            str(output_dir),
            str(file_path),
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip())

    return output_dir / f"{file_path.stem}.pdf"


def convert_image_to_pdf(file_path: Path) -> Path:
    """Convert an image file to PDF in place."""
    pdf_path = file_path.with_suffix(".pdf")
    with Image.open(file_path) as image:
        image.convert("RGB").save(pdf_path)
    return pdf_path


def collect_receipt_pdfs(declaration_dir: Path) -> list[Path]:
    """Collect all receipt files and convert them to PDF when needed."""
    pdf_paths: list[Path] = []

    for receipt_path in sorted(declaration_dir.iterdir()):
        if not receipt_path.is_file() or not receipt_path.name.startswith("bon_"):
            continue

        extension = receipt_path.suffix.lower()
        if extension == ".pdf":
            pdf_paths.append(receipt_path)
        elif extension in IMAGE_EXTENSIONS:
            pdf_paths.append(convert_image_to_pdf(receipt_path))
        elif extension in OFFICE_DOCUMENT_EXTENSIONS:
            pdf_paths.append(
                convert_office_document_to_pdf(receipt_path, declaration_dir)
            )
        else:
            print(f"Unsupported file format: {receipt_path.name}")

    return pdf_paths
