import os
import zipfile

def modify_docx_xml(docx_path, out_path):
    os.system(f"rm -rf /tmp/docx_v5_edit && mkdir -p /tmp/docx_v5_edit && unzip -q {docx_path} -d /tmp/docx_v5_edit")
    
    doc_xml_path = "/tmp/docx_v5_edit/word/document.xml"
    with open(doc_xml_path, 'r') as f:
        xml = f.read()

    # The exact string in XML
    target_str = ') [6]. The resulting density distributions'
    rep_str = ') [6]. This environmental benchmark dataset comprises 32 historically confirmed point-source rodent exposures. The resulting density distributions'
    xml = xml.replace(target_str, rep_str)
    
    with open(doc_xml_path, 'w') as f:
        f.write(xml)
        
    os.system(f"cd /tmp/docx_v5_edit && zip -q -r {os.path.abspath(out_path)} *")

if __name__ == "__main__":
    modify_docx_xml("docs/andes_virus_research_letter_v5.docx", "docs/andes_virus_research_letter_v5.docx")
