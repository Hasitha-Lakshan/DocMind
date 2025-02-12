import fitz  # PyMuPDF
import os

def read_pdf(file_name):
    file_path = os.path.join("input_files", file_name)
    
    if not os.path.exists(file_path):
        print(f"Error: File '{file_name}' not found in 'input_files' folder.")
        return
    
    try:
        doc = fitz.open(file_path)
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            text = page.get_text()
            print(f"Page {page_num + 1}:\n{text}\n{'-'*40}")
        
        doc.close()
    except Exception as e:
        print(f"Error reading PDF: {e}")

if __name__ == "__main__":
    pdf_file = "IRON_MOUNTAIN_SAR.pdf"  # Change this to your actual file name
    read_pdf(pdf_file)