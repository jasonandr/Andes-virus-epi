import os
import re

def fix_manuscript(docx_path, out_path):
    os.system(f"rm -rf /tmp/docx_v8_edit && mkdir -p /tmp/docx_v8_edit && unzip -q {docx_path} -d /tmp/docx_v8_edit")
    
    doc_xml_path = "/tmp/docx_v8_edit/word/document.xml"
    with open(doc_xml_path, 'r') as f:
        xml = f.read()

    # Regex for comment 6:
    # We want to replace the sequence starting with <w:commentRangeStart w:id="6"/>
    # and ending with %)
    # Let's find the indices!
    start_idx = xml.find('<w:commentRangeStart w:id="6"/>')
    end_str = '%)</w:t></w:r>'
    end_idx = xml.find(end_str, start_idx) + len(end_str)
    
    if start_idx != -1 and end_idx != -1:
        rep_6 = '<w:r w:rsidRPr="006F4BB0"><w:t xml:space="preserve">(&gt;80%, comprising 68.5% generating zero and 12.6% generating one)</w:t></w:r>'
        xml = xml[:start_idx] + rep_6 + xml[end_idx:]
        print("Replaced comment 6 text successfully.")
    else:
        print("Could not find indices for comment 6!")
    
    with open(doc_xml_path, 'w') as f:
        f.write(xml)
        
    os.system(f"cd /tmp/docx_v8_edit && zip -q -r {os.path.abspath(out_path)} *")
    print("Done generating", out_path)

if __name__ == "__main__":
    # Apply over the already processed v6!
    fix_manuscript("docs/andes_virus_research_letter_v6.docx", "docs/andes_virus_research_letter_v7.docx")
