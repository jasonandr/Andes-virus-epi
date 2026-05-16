import os
import zipfile

def modify_docx_xml(docx_path, out_path):
    os.system(f"rm -rf /tmp/docx_v4_edit && mkdir -p /tmp/docx_v4_edit && unzip -q {docx_path} -d /tmp/docx_v4_edit")
    
    doc_xml_path = "/tmp/docx_v4_edit/word/document.xml"
    with open(doc_xml_path, 'r') as f:
        xml = f.read()

    # Replacements
    xml = xml.replace('<w:t>78.5</w:t>', '<w:t>68.5</w:t>')
    
    # Superspreading
    xml = xml.replace('superspreading dynamics', 'transmission heterogeneity')
    
    # Add environmental info (we already did this in python-docx, let's see if we need to do it here)
    # Actually, the user's V4 still has '[6]' without the extra text, we can replace it here too.
    xml = xml.replace('<w:t>) [6].</w:t>', '<w:t>) [6]. This environmental benchmark dataset comprises 32 historically confirmed point-source rodent exposures.</w:t>')
    
    # First IQR
    target1 = '<w:t>IQR XX</w:t></w:r><w:r w:rsidR="0092471F"><w:t>.</w:t></w:r><w:r w:rsidR="00707A9B"><w:t>X-YY</w:t></w:r><w:r w:rsidR="0092471F"><w:t>.</w:t></w:r><w:r w:rsidR="00707A9B"><w:t>Y</w:t></w:r>'
    rep1 = '<w:t>IQR 14.8-27.2</w:t></w:r><w:r w:rsidR="0092471F"><w:t></w:t></w:r><w:r w:rsidR="00707A9B"><w:t></w:t></w:r><w:r w:rsidR="0092471F"><w:t></w:t></w:r><w:r w:rsidR="00707A9B"><w:t></w:t></w:r>'
    xml = xml.replace(target1, rep1)
    
    # Second IQR
    target2 = '<w:t>, IQR XX</w:t></w:r><w:commentRangeStart w:id="8"/><w:r w:rsidR="0092471F"><w:t>.X-YY</w:t></w:r><w:commentRangeEnd w:id="8"/><w:r w:rsidR="00CC1BDF"><w:rPr><w:rStyle w:val="CommentReference"/><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr><w:commentReference w:id="8"/></w:r><w:r w:rsidR="0092471F"><w:t>.Y</w:t></w:r>'
    rep2 = '<w:t>, IQR 13.8-24.7</w:t></w:r><w:commentRangeStart w:id="8"/><w:r w:rsidR="0092471F"><w:t></w:t></w:r><w:commentRangeEnd w:id="8"/><w:r w:rsidR="00CC1BDF"><w:rPr><w:rStyle w:val="CommentReference"/><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr><w:commentReference w:id="8"/></w:r><w:r w:rsidR="0092471F"><w:t></w:t></w:r>'
    xml = xml.replace(target2, rep2)
    
    with open(doc_xml_path, 'w') as f:
        f.write(xml)
        
    os.system(f"cd /tmp/docx_v4_edit && zip -q -r {os.path.abspath(out_path)} *")

if __name__ == "__main__":
    modify_docx_xml("docs/andes_virus_research_letter_v4.docx", "docs/andes_virus_research_letter_v5.docx")
