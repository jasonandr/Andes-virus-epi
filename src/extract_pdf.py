import os
try:
    import pdfplumber
except ImportError:
    os.system("pip3 install pdfplumber > /dev/null 2>&1")
    import pdfplumber

def main():
    pdf_path = "/Users/jasonandrews/repos/hanta/literature/nejmoa2009040_appendix_1.pdf"
    print(f"Extracting text from {os.path.basename(pdf_path)}")
    
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages):
            text = page.extract_text()
            if text:
                # Look for keywords related to transmission network or line list
                if any(kw in text.lower() for kw in ['transmission', 'network', 'onset', 'infector', 'case']):
                    print(f"\n--- Page {i+1} ---")
                    # print first 500 characters of the matching page to see if it's a table
                    print(text[:1000])

if __name__ == "__main__":
    main()
