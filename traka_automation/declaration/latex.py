import re
import subprocess
from pathlib import Path

TEMPLATE_PATH = Path(__file__).parent / "templates" / "declaration_form_template.tex"
FIELD_MAPPINGS = {
    "{{ name }}": "name",
    "{{ cost }}": "cost",
    "{{ IBAN }}": "IBAN",
    "{{ specification }}": "specification",
    "{{ description }}": "description",
    "{{ comments }}": "comments",
    "{{ submission_time }}": "submission_time",
    "{{ camp }}": "camp",
}


def load_template(template_path: Path = TEMPLATE_PATH) -> str:
    """Load the LaTeX declaration template."""
    return template_path.read_text(encoding="utf-8")


def compile_latex(tex_file: Path, output_dir: Path) -> None:
    """Compile a LaTeX file into a PDF."""
    subprocess.run(
        ["pdflatex", "-output-directory", str(output_dir), str(tex_file)],
        check=True,
    )


def tex_escape(text: str) -> str:
    """Escape plain text so it renders correctly in LaTeX."""
    conv = {
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\^{}",
        "\\": r"\textbackslash{}",
        "<": r"\textless{}",
        ">": r"\textgreater{}",
    }
    regex = re.compile(
        "|".join(re.escape(str(key)) for key in sorted(conv, key=lambda item: -len(item)))
    )
    return regex.sub(lambda match: conv[match.group()], str(text))


def build_receipt_include_commands(pdf_paths: list[Path]) -> str:
    """Render the LaTeX commands that embed the receipt PDFs."""
    return "".join(
        f"\\includepdf[pages={{1-}},scale=0.75]{{{pdf_path}}}\n"
        for pdf_path in pdf_paths
    )


def render_declaration(data: dict[str, str], receipt_pages: str) -> str:
    """Render declaration data into the LaTeX template."""
    rendered_latex = load_template()
    for placeholder, key in FIELD_MAPPINGS.items():
        rendered_latex = rendered_latex.replace(placeholder, tex_escape(data[key]))
    return rendered_latex.replace("{{ bonnen }}", receipt_pages)
