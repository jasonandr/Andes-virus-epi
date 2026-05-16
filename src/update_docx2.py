import os
import zipfile

def modify_docx_xml(docx_path, out_path):
    os.system(f"rm -rf /tmp/docx_v4_edit && mkdir -p /tmp/docx_v4_edit && unzip -q {docx_path} -d /tmp/docx_v4_edit")
    
    doc_xml_path = "/tmp/docx_v4_edit/word/document.xml"
    with open(doc_xml_path, 'r') as f:
        xml = f.read()

    # Replacements
    xml = xml.replace('78.5%', '68.5%')
    
    # Superspreading
    xml = xml.replace('superspreading dynamics', 'transmission heterogeneity')
    
    # IQR values
    # Because of xml tags, XX.X-YY.Y might be split, but let's check if it exists contiguously
    # Since we saw earlier it was contiguous enough for python-docx to find it? No, python-docx extracts pure text!
    # If we use python-docx, we lose formatting on that specific paragraph because p.text = p.text wipes out bold/italics in that paragraph!
    # Let's check if python-docx wiped out formatting. It does!
    pass

def use_python_docx_safe(docx_path, out_path):
    import docx
    doc = docx.Document(docx_path)
    for p in doc.paragraphs:
        if '78.5%' in p.text:
            # Safer way: iterate runs
            for r in p.runs:
                if '78.5%' in r.text:
                    r.text = r.text.replace('78.5%', '68.5%')
        if 'XX.X-YY.Y' in p.text:
            # We must be very careful. Let's just find the runs.
            # A run might just have "XX.X-YY.Y"
            found_first = False
            for r in p.runs:
                if 'XX.X-YY.Y' in r.text:
                    if not found_first:
                        r.text = r.text.replace('XX.X-YY.Y', '14.8-27.2')
                        found_first = True
                    else:
                        r.text = r.text.replace('XX.X-YY.Y', '13.8-24.7')
        if 'superspreading dynamics' in p.text:
            for r in p.runs:
                if 'superspreading dynamics' in r.text:
                    r.text = r.text.replace('superspreading dynamics', 'transmission heterogeneity')
                    
        # Add environmental info
        if 'rodent-to-human' in p.text and '[6]' in p.text:
            # Find the run with '[6]' and append the info
            for r in p.runs:
                if '[6]' in r.text and 'This environmental benchmark' not in p.text:
                    r.text = r.text.replace('[6]', '[6]. This environmental benchmark dataset comprises 32 historically confirmed point-source rodent exposures')
                    
    doc.save(out_path)

if __name__ == "__main__":
    use_python_docx_safe("docs/andes_virus_research_letter_v4.docx", "docs/andes_virus_research_letter_v5.docx")
