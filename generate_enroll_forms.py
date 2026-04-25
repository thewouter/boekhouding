import subprocess # Import subprocess module
from typing import Tuple

from docxtpl import DocxTemplate
import os
import json


def convert_docx_to_pdf(file_path, output_dir):
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


def template_form(json_data) -> Tuple[str, str]:
    print(os.getcwd())
    doc = DocxTemplate("/scratch/form_templates/scoutdoor.docx")
    doc.render(json_data)
    output_dir = f"onedrive/data/exchange_folder/inschrijfformulieren"
    output_file = f"{output_dir}/{json_data['name'].replace(' ','_')}-{json_data['camp']}.docx"
    doc.save(output_file)
    return output_file, output_dir


BASE_DIR = "/onedrive/data/exchange_folder/inschrijvingen"

def main():
    for root, dirs, files in os.walk(BASE_DIR):
        for file in files:
            if file.endswith(".json"):
                path = os.path.join(root, file)
                print(f"Found JSON: {path}")

                # Optional: safely load the JSON file
                # try:
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    docx_file, output_dir = template_form(data)
                    print(docx_file)
                    print(output_dir)
                    convert_docx_to_pdf(docx_file, output_dir)
                    # Example placeholder for processing
                    # print(data.keys())

                # except Exception as e:
                #     print(f"Failed to read {path}: {e}")

if __name__ == '__main__':
    print("Generating enroll forms")
    main()
