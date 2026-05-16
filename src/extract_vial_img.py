import fitz
import sys

doc = fitz.open('literature/Vial - incubation period of Andes virus - EID 2006.pdf')
for i in range(len(doc)):
    for img in doc.get_page_images(i):
        xref = img[0]
        pix = fitz.Pixmap(doc, xref)
        if pix.n - pix.alpha > 3:
            pix = fitz.Pixmap(fitz.csRGB, pix)
        pix.save(f"data/vial_img_p{i}_{xref}.png")
        pix = None
print("Extracted images")
