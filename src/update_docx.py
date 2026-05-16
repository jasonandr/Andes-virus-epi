import docx
import sys

def replace_text_in_runs(runs, old_text, new_text):
    # This is a naive replacement that requires the whole old_text to be within a single run.
    # It might fail if word splits it. But we'll try it first on paragraph text.
    pass

def replace_in_paragraphs(paragraphs):
    for p in paragraphs:
        if '14 secondary cases' in p.text:
            p.text = p.text.replace('14 secondary cases', '16 cases')
        if '14' in p.text and 'Bolson' in p.text:
            p.text = p.text.replace('14', '16')
        if '0.23' in p.text:
            p.text = p.text.replace('0.23', '0.24')
        if '68.5%' in p.text:
            p.text = p.text.replace('68.5%', '69.5%')
        if 'k = 0.23' in p.text:
            p.text = p.text.replace('k = 0.23', 'k = 0.24')

def main():
    doc = docx.Document('drafts/andes_virus_research_letter_v10.docx')
    replace_in_paragraphs(doc.paragraphs)
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                replace_in_paragraphs(cell.paragraphs)
    doc.save('drafts/andes_virus_research_letter_v11.docx')
    print("Saved v11.docx")

if __name__ == '__main__':
    main()
