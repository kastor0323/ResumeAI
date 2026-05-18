import PyPDF2
import sys

def extract_text(pdf_path, out_path):
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ''
            for page in reader.pages:
                text += page.extract_text() + '\n'
            with open(out_path, 'w', encoding='utf-8') as out_file:
                out_file.write(text)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    extract_text(sys.argv[1], sys.argv[2])
