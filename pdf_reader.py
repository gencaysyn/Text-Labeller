import sys, fitz
import re

class PDFHandler:
    def __init__(self, name):
        self.current_page = 0
        self.pdf = fitz.open(name)
        self.num_pages = self.pdf.pageCount

    def nextPage(self):
        if self.current_page < self.num_pages -1:
            self.current_page += 1
    
    def prevPage(self):
        if self.current_page > 0:
            self.current_page -= 1

    def toImage(self):
        # return self.pdf.getPagePixmap(self.current_page)
        page = self.pdf[self.current_page]
        blocks = page.getText("blocks")
        _, page = self.handleBlocks(blocks, page)
        return page.getPixmap(alpha=False)
        # return self.pdf[self.current_page].getPixmap(alpha=False)

    def handleBlocks(self, blocks, page):
        text = ""
        i = 0
        max_ = len(blocks)
        annot_started = False
        for b in blocks:
            t  = re.sub(r"\n\s*", "", b[4])
            t_ = t.replace(' ', '')
            if t_.startswith("*") or t_.startswith("�") or t_.startswith("•"):
                annot_started = True
            
            if annot_started or len(t) < 10:
                page.drawRect(fitz.Rect(b[:-3]), color=(1, 0, 0))
            else:
                page.drawRect(fitz.Rect(b[:-3]), color=(0, 1, 0))
                text += t + " "
            i += 1
        return text, page

    def toText(self):
        blocks = self.pdf[7].getText("blocks")
        page = self.handleBlocks(blocks, self.pdf[7])    

        pdfText = ""
        for i in range(self.current_page, self.num_pages):  # iterate the document pages
            page = self.pdf[i]
            blocks = page.getText("blocks")
            text, _ = self.handleBlocks(blocks, page)
            if text  is not None:
                pdfText += text + " "
        return pdfText


if __name__ == "__main__":
    print(PDFHandler("test.pdf").toText())