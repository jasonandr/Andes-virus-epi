import os
import re

def fix_manuscript(docx_path, out_path):
    os.system(f"rm -rf /tmp/docx_v7_edit && mkdir -p /tmp/docx_v7_edit && unzip -q {docx_path} -d /tmp/docx_v7_edit")
    
    doc_xml_path = "/tmp/docx_v7_edit/word/document.xml"
    with open(doc_xml_path, 'r') as f:
        xml = f.read()

    # Regex for comment 4:
    # Match everything from <w:commentRangeStart w:id="4"/> up to the period after cohort.
    xml = re.sub(
        r'<w:commentRangeStart w:id="4"/>.*?<w:t>cohort</w:t>.*?</w:r>.*?<w:t xml:space="preserve">\. </w:t></w:r>',
        r'<w:r w:rsidR="000D50AE"><w:t xml:space="preserve">cohort. For comparison, we modeled the distribution of environmental (rodent-to-human) incubation periods using 32 point-source exposures from historical literature [6]. </w:t></w:r>',
        xml, flags=re.DOTALL
    )
    
    # Regex for comment 6:
    # Match everything from <w:commentRangeStart w:id="6"/> up to %)</w:t></w:r>
    xml = re.sub(
        r'<w:commentRangeStart w:id="6"/>.*?>&gt;8.*?</w:t></w:r>.*?<w:t xml:space="preserve">%\)</w:t></w:r>',
        r'<w:r w:rsidRPr="006F4BB0"><w:t xml:space="preserve">(&gt;80%, comprising 68.5% generating zero and 12.6% generating one)</w:t></w:r>',
        xml, flags=re.DOTALL
    )
    
    with open(doc_xml_path, 'w') as f:
        f.write(xml)
        
    os.system(f"cd /tmp/docx_v7_edit && zip -q -r {os.path.abspath(out_path)} *")
    print("Done generating", out_path)

if __name__ == "__main__":
    fix_manuscript("docs/andes_virus_research_letter_v5.docx", "docs/andes_virus_research_letter_v6.docx")
