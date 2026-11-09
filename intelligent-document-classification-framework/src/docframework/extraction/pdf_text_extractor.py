from docframework.core.pdf_document import PDFDocument
from docframework.core.extracted_page import ExtractedPage
import pymupdf


class PDFTextExtractor:
    def extract(self, document: PDFDocument) -> list[ExtractedPage]:
      extracted_pages: list[ExtractedPage] = []

      with pymupdf.open(document.file_path) as doc:
         for index,page in enumerate(doc,start=1):
            extracted_pages.append(
                ExtractedPage(page_number=index,content_page=page.get_text())
            )

      return extracted_pages
   
