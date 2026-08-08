import json
from pathlib import Path

from traka_automation.declaration.processor import (
    process_all_declarations,
    process_declaration,
)


def test_process_all_declarations_processes_directories_in_sorted_order(
    monkeypatch, tmp_path: Path
):
    processed: list[tuple[Path, Path]] = []
    declarations_dir = tmp_path / "declarations"
    declarations_dir.mkdir()
    output_dir = tmp_path / "output"
    output_dir.mkdir()

    for directory_name in ("b-dir", "a-dir"):
        (declarations_dir / directory_name).mkdir()
    (declarations_dir / "not-a-dir.txt").write_text("ignored", encoding="utf-8")

    def fake_process_declaration(declaration_dir: Path, passed_output_dir: Path) -> None:
        processed.append((declaration_dir, passed_output_dir))

    monkeypatch.setattr(
        "traka_automation.declaration.processor.process_declaration",
        fake_process_declaration,
    )

    process_all_declarations(declarations_dir, output_dir)

    assert processed == [
        (declarations_dir / "a-dir", output_dir),
        (declarations_dir / "b-dir", output_dir),
    ]


def test_process_declaration_writes_pdf_and_cleans_up(monkeypatch, tmp_path: Path):
    declaration_dir = tmp_path / "decl-123"
    declaration_dir.mkdir()
    output_dir = tmp_path / "out"
    output_dir.mkdir()
    (declaration_dir / "data.json").write_text(json.dumps({"name": "ignored"}), encoding="utf-8")

    data = {
        "name": "Alice",
        "cost": "10.00",
        "IBAN": "NL00BANK0123",
        "specification": "Spec",
        "description": "Desc",
        "comments": "Comment",
        "submission_time": "2026-08-08",
        "camp": "Summer Camp",
    }
    pdf_paths = [declaration_dir / "bon_1.pdf"]

    def fake_compile_latex(tex_file: Path, passed_output_dir: Path) -> None:
        filename = tex_file.stem
        (passed_output_dir / f"{filename}.aux").write_text("aux", encoding="utf-8")
        (passed_output_dir / f"{filename}.log").write_text("log", encoding="utf-8")
        (passed_output_dir / f"{filename}.pdf").write_text("pdf", encoding="utf-8")

    monkeypatch.setattr("traka_automation.declaration.processor.load_json", lambda _: data)
    monkeypatch.setattr(
        "traka_automation.declaration.processor.collect_receipt_pdfs",
        lambda _: pdf_paths,
    )
    monkeypatch.setattr(
        "traka_automation.declaration.processor.build_receipt_include_commands",
        lambda paths: "PDF-COMMANDS" if paths == pdf_paths else "",
    )
    monkeypatch.setattr(
        "traka_automation.declaration.processor.render_declaration",
        lambda passed_data, receipt_pages: (
            "LATEX-CONTENT"
            if passed_data == data and receipt_pages == "PDF-COMMANDS"
            else "WRONG"
        ),
    )
    monkeypatch.setattr(
        "traka_automation.declaration.processor.compile_latex",
        fake_compile_latex,
    )

    process_declaration(declaration_dir, output_dir)

    output_pdf = output_dir / "declaratie_decl-123.pdf"
    assert output_pdf.exists()
    assert output_pdf.read_text(encoding="utf-8") == "pdf"
    assert not declaration_dir.exists()
