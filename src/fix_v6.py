import os

def fix_manuscript(docx_path, out_path):
    os.system(f"rm -rf /tmp/docx_fix_edit && mkdir -p /tmp/docx_fix_edit && unzip -q {docx_path} -d /tmp/docx_fix_edit")
    
    doc_xml_path = "/tmp/docx_fix_edit/word/document.xml"
    with open(doc_xml_path, 'r') as f:
        xml = f.read()

    # Fix comment 4
    start_str_4 = '<w:commentRangeStart w:id="4"/>'
    end_str_4 = '<w:t xml:space="preserve">. </w:t></w:r>'
    
    s4 = xml.find(start_str_4)
    e4 = xml.find(end_str_4, s4) + len(end_str_4)
    if s4 != -1 and e4 != -1:
        rep_4 = '<w:r w:rsidR="000D50AE"><w:t xml:space="preserve">cohort. For comparison, we modeled the distribution of environmental (rodent-to-human) incubation periods using 32 point-source exposures from historical literature [6]. </w:t></w:r>'
        xml = xml[:s4] + rep_4 + xml[e4:]
    else:
        print("Failed to find comment 4")

    # Fix comment 6
    start_str_6 = '<w:commentRangeStart w:id="6"/>'
    end_str_6 = '%) generated zero </w:t></w:r>'
    
    s6 = xml.find(start_str_6)
    e6 = xml.find(end_str_6, s6) + len(end_str_6)
    if s6 != -1 and e6 != -1:
        rep_6 = '<w:r w:rsidRPr="006F4BB0"><w:t xml:space="preserve">(&gt;80%, comprising 68.5% generating zero and 12.6% generating one) generated zero </w:t></w:r>'
        xml = xml[:s6] + rep_6 + xml[e6:]
    else:
        print("Failed to find comment 6")
        
    with open(doc_xml_path, 'w') as f:
        f.write(xml)
        
    os.system(f"cd /tmp/docx_fix_edit && zip -q -r {os.path.abspath(out_path)} *")
    print("Done generating", out_path)

if __name__ == "__main__":
    fix_manuscript("docs/andes_virus_research_letter_v5.docx", "docs/andes_virus_research_letter_v6.docx")
