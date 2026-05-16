import docx
import re
import zipfile

def modify_docx_xml(docx_path, out_path):
    # Unpack
    import os
    os.system(f"rm -rf /tmp/docx_v4_edit && mkdir -p /tmp/docx_v4_edit && unzip -q {docx_path} -d /tmp/docx_v4_edit")
    
    doc_xml_path = "/tmp/docx_v4_edit/word/document.xml"
    with open(doc_xml_path, 'r') as f:
        xml = f.read()

    # The text we want to replace might be broken up by tags.
    # To do this safely without an XML parser:
    # 1. 78.5% -> 68.5%
    # In XML, numbers are rarely split. Let's just do a direct string replace
    xml = xml.replace('78.5%', '68.5%')
    
    # 2. IQR XX.X-YY.Y
    # There are two of these. First one is H2H: 14.8-27.2
    # Second is Env: 13.8-24.7
    # Let's replace the first instance with 14.8-27.2, and second with 13.8-24.7
    if "XX.X-YY.Y" in xml:
        xml = xml.replace("XX.X-YY.Y", "14.8-27.2", 1)
        xml = xml.replace("XX.X-YY.Y", "13.8-24.7", 1)
    else:
        # It might be split like XX.X</w:t><w:r><w:t>-YY.Y
        # We can strip tags, but it's hard to put them back.
        # Let's just use python-docx if XML replacement fails.
        pass
        
    with open(doc_xml_path, 'w') as f:
        f.write(xml)
        
    os.system(f"cd /tmp/docx_v4_edit && zip -q -r {os.path.abspath(out_path)} *")

def use_python_docx(docx_path, out_path):
    doc = docx.Document(docx_path)
    for p in doc.paragraphs:
        if '78.5%' in p.text:
            p.text = p.text.replace('78.5%', '68.5%')
        if 'XX.X-YY.Y' in p.text:
            # First is H2H, second is Env. We can replace sequentially if they are in the same or different paragraphs.
            if 'human-to-human' in p.text.lower() or '20.1' in p.text:
                p.text = p.text.replace('XX.X-YY.Y', '14.8-27.2')
            if 'environmental' in p.text.lower() or '18.5' in p.text:
                p.text = p.text.replace('XX.X-YY.Y', '13.8-24.7')
        if 'superspreading dynamics' in p.text:
            p.text = p.text.replace('superspreading dynamics', 'transmission heterogeneity')
            
    doc.save(out_path)

if __name__ == "__main__":
    # Let's try python-docx first. If it destroys comments, we know.
    use_python_docx("docs/andes_virus_research_letter_v4.docx", "/tmp/test_v5.docx")
    
    # Check if comments.xml exists in the new file
    import zipfile
    with zipfile.ZipFile("/tmp/test_v5.docx", 'r') as z:
        if 'word/comments.xml' in z.namelist():
            print("python-docx preserved comments!")
            os.system("cp /tmp/test_v5.docx docs/andes_virus_research_letter_v5.docx")
        else:
            print("python-docx destroyed comments. Falling back to XML hack.")
            modify_docx_xml("docs/andes_virus_research_letter_v4.docx", "docs/andes_virus_research_letter_v5.docx")
