from pathlib import Path
from subprocess import CompletedProcess

from PIL import Image

from traka_automation.declaration.conversion import (
    collect_receipt_pdfs,
    convert_image_to_pdf,
    convert_office_document_to_pdf,
)


def test_convert_office_document_to_pdf_calls_libreoffice(monkeypatch):
    calls: list[list[str]] = []

    def fake_run(command: list[str], capture_output: bool, text: bool, check: bool):
        calls.append(command)
        assert capture_output is True
        assert text is True
        assert check is False
        return CompletedProcess(command, 0, stdout="ok", stderr="")

    monkeypatch.setattr("traka_automation.declaration.conversion.subprocess.run", fake_run)

    file_path = Path("/tmp/bonnen.xlsx")
    output_dir = Path("/tmp/output")
    pdf_path = convert_office_document_to_pdf(file_path, output_dir)

    assert pdf_path == output_dir / "bonnen.pdf"
    assert calls == [
        [
            "libreoffice",
            "--headless",
            "--convert-to",
            "pdf",
            "--outdir",
            str(output_dir),
            str(file_path),
        ]
    ]


def test_convert_office_document_to_pdf_raises_on_failure(monkeypatch):
    def fake_run(command: list[str], capture_output: bool, text: bool, check: bool):
        return CompletedProcess(command, 1, stdout="", stderr="broken")

    monkeypatch.setattr("traka_automation.declaration.conversion.subprocess.run", fake_run)

    try:
        convert_office_document_to_pdf(Path("/tmp/bon.docx"), Path("/tmp"))
    except RuntimeError as exc:
        assert str(exc) == "broken"
    else:
        raise AssertionError("Expected RuntimeError")


def test_convert_image_to_pdf(tmp_path: Path):
    image_path = tmp_path / "bon_image.png"
    Image.new("RGB", (10, 10), color="red").save(image_path)

    pdf_path = convert_image_to_pdf(image_path)

    assert pdf_path == tmp_path / "bon_image.pdf"
    assert pdf_path.exists()


def test_collect_receipt_pdfs_converts_supported_files(monkeypatch, tmp_path: Path):
    pdf_receipt = tmp_path / "bon_1.pdf"
    image_receipt = tmp_path / "bon_2.png"
    office_receipt = tmp_path / "bon_3.xlsx"
    unsupported_receipt = tmp_path / "bon_4.txt"
    ignored_file = tmp_path / "notes.txt"

    for path in (
        pdf_receipt,
        image_receipt,
        office_receipt,
        unsupported_receipt,
        ignored_file,
    ):
        path.write_text("x", encoding="utf-8")

    converted_image = tmp_path / "converted-image.pdf"
    converted_office = tmp_path / "converted-office.pdf"
    image_calls: list[Path] = []
    office_calls: list[tuple[Path, Path]] = []

    def fake_image_converter(file_path: Path) -> Path:
        image_calls.append(file_path)
        return converted_image

    def fake_office_converter(file_path: Path, output_dir: Path) -> Path:
        office_calls.append((file_path, output_dir))
        return converted_office

    monkeypatch.setattr(
        "traka_automation.declaration.conversion.convert_image_to_pdf",
        fake_image_converter,
    )
    monkeypatch.setattr(
        "traka_automation.declaration.conversion.convert_office_document_to_pdf",
        fake_office_converter,
    )

    pdf_paths = collect_receipt_pdfs(tmp_path)

    assert pdf_paths == [pdf_receipt, converted_image, converted_office]
    assert image_calls == [image_receipt]
    assert office_calls == [(office_receipt, tmp_path)]
