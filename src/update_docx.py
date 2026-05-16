import docx
import sys

def replace_in_paragraphs(paragraphs):
    for p in paragraphs:
        if '18.5' in p.text:
            p.text = p.text.replace('18.5', '18.3')

def main():
    doc = docx.Document('drafts/andes_virus_research_letter_v11.docx')
    replace_in_paragraphs(doc.paragraphs)
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                replace_in_paragraphs(cell.paragraphs)
    doc.save('drafts/andes_virus_research_letter_v12.docx')
    print("Saved v12.docx")

if __name__ == '__main__':
    main()
