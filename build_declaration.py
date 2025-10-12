import os
import json
import re
import shutil
import subprocess

from PIL import Image

def convert_xlsx_to_pdf(file_path, output_dir):
    result = subprocess.run([
        "libreoffice",
        "--headless",
        "--convert-to", "pdf",
        "--outdir", output_dir,
        file_path
    ], capture_output=False, text=True)

    if result.returncode != 0:
        raise RuntimeError(f"LibreOffice failed: {result.stderr}")

    return os.path.join(
        output_dir,
        os.path.splitext(os.path.basename(file_path))[0] + ".pdf"
    )


def load_template(template_path):
    with open(template_path, "r") as f:
        return f.read()

def compile_latex(tex_file, out_dir):
    subprocess.run(["pdflatex", '-output-directory', out_dir, tex_file], check=True)

def tex_escape(text):
    """
        :param text: a plain text message
        :return: the message escaped to appear correctly in LaTeX
    """
    conv = {
        '&': r'\&',
        '%': r'\%',
        '$': r'\$',
        '#': r'\#',
        '_': r'\_',
        '{': r'\{',
        '}': r'\}',
        '~': r'\textasciitilde{}',
        '^': r'\^{}',
        '\\': r'\textbackslash{}',
        '<': r'\textless{}',
        '>': r'\textgreater{}',
    }
    regex = re.compile('|'.join(re.escape(str(key)) for key in sorted(conv.keys(), key=lambda item: - len(item))))
    return regex.sub(lambda match: conv[match.group()], text)


def main():
    directories = os.walk('/onedrive/data/exchange_folder/declaraties')
    main_dir = next(directories)
    for directory in main_dir[1]:
        print(main_dir)
        decla_dir = f"{main_dir[0]}/{directory}"
        with open(f"{decla_dir}/data.json") as json_file:
            data = json.load(json_file)
            print(data)

            invoice_files = sorted([f for f in os.listdir(decla_dir) if f.startswith("bon_")])

            pdf_paths = []
            for invoice in invoice_files:
                invoice_path = os.path.join(decla_dir, invoice)
                ext = os.path.splitext(invoice_path)[1].lower()

                if ext == ".pdf":
                    pdf_paths.append(invoice_path)
                elif ext in [".jpg", ".jpeg", ".png", ".bmp", ".tiff"]:
                    image = Image.open(invoice_path)
                    pdf_path = os.path.splitext(invoice_path)[0] + ".pdf"
                    image.convert("RGB").save(pdf_path)
                    pdf_paths.append(pdf_path)
                elif ext in [".xlsx", ".docx"]:
                    pdf_path = convert_xlsx_to_pdf(invoice_path, decla_dir)
                    pdf_paths.append(pdf_path)
                else:
                    print(f"Unsupported file format: {invoice}")

            pdf_command = ""
            for path in pdf_paths:
                pdf_command += f"\\includepdf[pages={{1-}},scale=0.75]{{{ path }}}\n"

            latex_template = load_template("/scratch/template.tex")
            rendered_latex = latex_template.replace("{{ name }}", tex_escape(data["name"]))
            rendered_latex = rendered_latex.replace("{{ cost }}", tex_escape(data["cost"]))
            rendered_latex = rendered_latex.replace("{{ IBAN }}", tex_escape(data["IBAN:"]))
            rendered_latex = rendered_latex.replace("{{ specification }}", tex_escape(data["specification"]))
            rendered_latex = rendered_latex.replace("{{ description }}", tex_escape(data["description"]))
            rendered_latex = rendered_latex.replace("{{ comments }}", tex_escape(data["comments"]))
            rendered_latex = rendered_latex.replace("{{ submission_time }}", tex_escape(data["submission_time"]))
            rendered_latex = rendered_latex.replace("{{ camp }}", tex_escape(data["camp"]))
            rendered_latex = rendered_latex.replace("{{ bonnen }}", pdf_command)

            filename = f"declaratie_{directory}"
            tex_file = f"{filename}.tex"
            with open(tex_file, "w") as f:
                f.write(rendered_latex)
            compile_latex(tex_file, decla_dir)

            os.remove(f"{decla_dir}/{filename}.aux")
            os.remove(f"{decla_dir}/{filename}.log")
            shutil.copyfile(f"{decla_dir}/{filename}.pdf", f"/onedrive/data/exchange_folder/declaratieformulieren/{filename}.pdf")
            shutil.rmtree(decla_dir)

if __name__ == '__main__':
    main()
