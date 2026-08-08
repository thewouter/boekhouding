from pathlib import Path

from traka_automation.declaration.latex import (
    TEMPLATE_PATH,
    build_receipt_include_commands,
    load_template,
    render_declaration,
    tex_escape,
)


def test_template_path_points_to_packaged_template():
    assert TEMPLATE_PATH.name == "declaration_form_template.tex"
    assert TEMPLATE_PATH.parent.name == "templates"


def test_load_template_reads_file(tmp_path: Path):
    template_path = tmp_path / "template.tex"
    template_path.write_text("hello", encoding="utf-8")

    assert load_template(template_path) == "hello"


def test_tex_escape_escapes_special_characters():
    assert tex_escape(r"&%$#_{}~^\<>") == (
        r"\&\%\$\#\_\{\}\textasciitilde{}\^{}\textbackslash{}\textless{}\textgreater{}"
    )


def test_build_receipt_include_commands_renders_all_pdfs():
    pdf_paths = [Path("/tmp/a.pdf"), Path("/tmp/b.pdf")]

    assert build_receipt_include_commands(pdf_paths) == (
        r"\includepdf[pages={1-},scale=0.75]{/tmp/a.pdf}"
        "\n"
        r"\includepdf[pages={1-},scale=0.75]{/tmp/b.pdf}"
        "\n"
    )


def test_render_declaration_substitutes_and_escapes_fields(monkeypatch):
    template = (
        "{{ name }}|{{ cost }}|{{ IBAN }}|{{ specification }}|{{ description }}|"
        "{{ comments }}|{{ submission_time }}|{{ camp }}|{{ bonnen }}"
    )
    data = {
        "name": "A&B",
        "cost": "12_50",
        "IBAN": "NL00BANK0123",
        "specification": "Spec%ial",
        "description": "Desc#ription",
        "comments": r"Contains\slash",
        "submission_time": "2026-08-08",
        "camp": "Camp~Name",
    }

    monkeypatch.setattr(
        "traka_automation.declaration.latex.load_template", lambda: template
    )

    rendered = render_declaration(data, "PDFS")

    assert rendered == (
        r"A\&B|12\_50|NL00BANK0123|Spec\%ial|Desc\#ription|"
        r"Contains\textbackslash{}slash|2026-08-08|Camp\textasciitilde{}Name|PDFS"
    )
