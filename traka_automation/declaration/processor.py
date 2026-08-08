import shutil
from pathlib import Path

from traka_automation.declaration.conversion import collect_receipt_pdfs
from traka_automation.declaration.latex import (
    build_receipt_include_commands,
    compile_latex,
    render_declaration,
)
from traka_automation.util.load_json import load_json

DECLARATIONS_DIR = Path("/onedrive/data/exchange_folder/declaraties")
OUTPUT_DIR = Path("/onedrive/data/exchange_folder/declaratieformulieren")


def process_all_declarations(
    declarations_dir: Path = DECLARATIONS_DIR, output_dir: Path = OUTPUT_DIR
) -> None:
    """Process every declaration directory in the exchange folder."""
    for declaration_dir in sorted(
        path for path in declarations_dir.iterdir() if path.is_dir()
    ):
        process_declaration(declaration_dir, output_dir)


def process_declaration(declaration_dir: Path, output_dir: Path = OUTPUT_DIR) -> None:
    """Build the final declaration PDF for a single declaration folder."""
    print(f"Processing declaration {declaration_dir.name}")
    data = load_json(declaration_dir / "data.json")
    pdf_paths = collect_receipt_pdfs(declaration_dir)
    receipt_pages = build_receipt_include_commands(pdf_paths)
    rendered_latex = render_declaration(data, receipt_pages)

    filename = f"declaratie_{declaration_dir.name}"
    tex_file = declaration_dir / f"{filename}.tex"
    tex_file.write_text(rendered_latex, encoding="utf-8")
    compile_latex(tex_file, declaration_dir)

    for extension in (".aux", ".log"):
        (declaration_dir / f"{filename}{extension}").unlink(missing_ok=True)

    shutil.copyfile(
        declaration_dir / f"{filename}.pdf",
        output_dir / f"{filename}.pdf",
    )
    shutil.rmtree(declaration_dir)
