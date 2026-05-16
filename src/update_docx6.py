import os
import zipfile
from lxml import etree

def fix_manuscript(docx_path, out_path):
    os.system(f"rm -rf /tmp/docx_v6_edit && mkdir -p /tmp/docx_v6_edit && unzip -q {docx_path} -d /tmp/docx_v6_edit")
    
    doc_xml_path = "/tmp/docx_v6_edit/word/document.xml"
    with open(doc_xml_path, 'r') as f:
        xml = f.read()

    # We want to replace the text around cohort to add the rodent-to-human info.
    # Current text in XML:
    # <w:commentRangeStart w:id="4"/><w:r w:rsidR="000D50AE"><w:t>cohort</w:t></w:r><w:commentRangeEnd w:id="4"/><w:r w:rsidR="001312B7"><w:rPr><w:rStyle w:val="CommentReference"/><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr><w:commentReference w:id="4"/></w:r><w:r w:rsidR="000D50AE"><w:t xml:space="preserve">. </w:t></w:r>
    
    # We will replace that whole block!
    target_4 = '<w:commentRangeStart w:id="4"/><w:r w:rsidR="000D50AE"><w:t>cohort</w:t></w:r><w:commentRangeEnd w:id="4"/><w:r w:rsidR="001312B7"><w:rPr><w:rStyle w:val="CommentReference"/><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr><w:commentReference w:id="4"/></w:r><w:r w:rsidR="000D50AE"><w:t xml:space="preserve">. </w:t></w:r>'
    rep_4 = '<w:r w:rsidR="000D50AE"><w:t xml:space="preserve">cohort. For comparison, we modeled the distribution of environmental (rodent-to-human) incubation periods using 32 point-source exposures from historical literature [6]. </w:t></w:r>'
    
    if target_4 in xml:
        xml = xml.replace(target_4, rep_4)
        print("Replaced comment 4 text successfully.")
    else:
        print("Could not find target 4!")
        
    # For comment 6, we want to clarify the >80% and remove the comment
    # Current text:
    # <w:commentRangeStart w:id="6"/><w:r w:rsidRPr="006F4BB0"><w:t>(</w:t></w:r><w:r w:rsidR="00B3539E" w:rsidRPr="006F4BB0"><w:t>&gt;8</w:t></w:r><w:r w:rsidRPr="006F4BB0"><w:t>0</w:t></w:r><w:commentRangeEnd w:id="6"/><w:r w:rsidR="00734BBD" w:rsidRPr="006F4BB0"><w:rPr><w:rStyle w:val="CommentReference"/><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr><w:commentReference w:id="6"/></w:r><w:r w:rsidRPr="006F4BB0"><w:t xml:space="preserve">%)</w:t></w:r>
    
    target_6 = '<w:commentRangeStart w:id="6"/><w:r w:rsidRPr="006F4BB0"><w:t>(</w:t></w:r><w:r w:rsidR="00B3539E" w:rsidRPr="006F4BB0"><w:t>&gt;8</w:t></w:r><w:r w:rsidRPr="006F4BB0"><w:t>0</w:t></w:r><w:commentRangeEnd w:id="6"/><w:r w:rsidR="00734BBD" w:rsidRPr="006F4BB0"><w:rPr><w:rStyle w:val="CommentReference"/><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr><w:commentReference w:id="6"/></w:r><w:r w:rsidRPr="006F4BB0"><w:t xml:space="preserve">%)</w:t></w:r>'
    rep_6 = '<w:r w:rsidRPr="006F4BB0"><w:t xml:space="preserve">(&gt;80%, comprising 68.5% generating zero and 12.6% generating one)</w:t></w:r>'
    
    if target_6 in xml:
        xml = xml.replace(target_6, rep_6)
        print("Replaced comment 6 text successfully.")
    else:
        print("Could not find target 6!")
    
    with open(doc_xml_path, 'w') as f:
        f.write(xml)
        
    os.system(f"cd /tmp/docx_v6_edit && zip -q -r {os.path.abspath(out_path)} *")

if __name__ == "__main__":
    fix_manuscript("docs/andes_virus_research_letter_v5.docx", "docs/andes_virus_research_letter_v6.docx")
