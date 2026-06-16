import os
try:
    import pypdf
except ImportError:
    import subprocess
    subprocess.check_call(["pip", "install", "pypdf"])
    import pypdf

def extract_pdf_text(pdf_path):
    reader = pypdf.PdfReader(pdf_path)
    text = ""
    for i, page in enumerate(reader.pages):
        text += f"--- Page {i+1} ---\n"
        text += page.extract_text() or ""
        text += "\n"
    return text

pdf_path = r"d:\Coding\자기소개서\2_target_companies\job_posting\IBK_26년 하계 청년인턴_직무기술서.pdf"
output_path = r"d:\Coding\자기소개서\2_target_companies\job_posting\IBK_26년 하계 청년인턴_직무기술서.txt"

if os.path.exists(pdf_path):
    text = extract_pdf_text(pdf_path)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"Successfully extracted text to {output_path}")
else:
    print(f"File not found: {pdf_path}")
