#!/usr/bin/env python3

import pdfrw
inputpdf = pdfrw.PdfReader("Frenoy2018.pdf")

logo = pdfrw.PdfReader("logo_raven.pdf").pages[0]
size_x=15
size_y=None
x_offset=1
y_offset=3

found_doi=set()

for page in inputpdf.pages:
    for i in range(len(page.Annots)):
        annot = page.Annots[i]
        link = annot['/A']
        if not link:
            continue
        uri = link['/URI'].to_unicode()
        if 'https://doi.org' in uri:
            if uri in found_doi:  # We already saw this DOI before
                continue
            found_doi.add(uri)
            # Find the sci-hub url
            newlink = pdfrw.objects.pdfstring.PdfString.from_unicode(uri.replace("doi.org","sci-hub.tw"))
            # Create a new hypertext link in the pdf
            # pdfrw does not provide functions for deep copy, so we have to improvise
            newannot = pdfrw.objects.pdfdict.PdfDict(annot)
            newannot.Subtype = annot['/Subtype']
            newannot.P = annot['/P']
            newannot.F = annot['/F']
            newannot.BS = annot['/BS']
            newannot.Border = annot['/Border']
            newannot.A = pdfrw.objects.pdfdict.PdfDict(annot['/A'])
            newannot.A.URI = newlink
            newannot.Rect = pdfrw.objects.pdfarray.PdfArray(annot['/Rect'])
            # Scale the sci-hub logo so we can compute the position of this link
            wmark = pdfrw.PageMerge().add(logo)[0]
            if size_x:
                wmark.scale(size_x / wmark.w)
            elif size_y:
                wmark.scale(size_y / wmark.h)
            # Finish computing the position of the link and actually add it to the pdf
            xlink = float(annot['/Rect'][2])
            ylink = float(annot['/Rect'][1])
            hlink = float(annot['/Rect'][3]) - float(annot['/Rect'][1])
            wlink = float(annot['/Rect'][2]) - float(annot['/Rect'][0])
            newannot.Rect[0] = pdfrw.objects.pdfobject.PdfObject(str(xlink + x_offset))
            newannot.Rect[2] = pdfrw.objects.pdfobject.PdfObject(str(wmark.w + xlink + x_offset))
            wmark.x = float(newannot.Rect[0])
            newannot.Rect[1] = pdfrw.objects.pdfobject.PdfObject(str(ylink + y_offset + hlink/2 - wmark.h/2))
            newannot.Rect[3] = pdfrw.objects.pdfobject.PdfObject(str(ylink + y_offset + hlink/2 + wmark.h/2))
            wmark.y = ylink + y_offset + hlink/2 - wmark.h/2
            page.Annots.append(newannot)
            pdfrw.PageMerge(page).add(wmark).render()


pdfrw.PdfWriter("test_add2.pdf", trailer=inputpdf).write()
