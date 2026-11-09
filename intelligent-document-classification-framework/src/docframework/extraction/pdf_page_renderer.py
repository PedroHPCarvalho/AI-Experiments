from docframework.core.rendered_page import RenderedPage
from docframework.core.pdf_document import PDFDocument
import pymupdf

class PDFPageRenderer:
  def render(self, document: PDFDocument, dpi: int = 150) -> list[RenderedPage]:
    rendered_pages: list[RenderedPage] = []

    with pymupdf.open(document.file_path) as doc:
      for index,page in enumerate(doc,start=1):
        render_page = page.get_pixmap(dpi=dpi)
        rendered_pages.append(
          RenderedPage(
            page_number=index,
            image_bytes=render_page.tobytes("png"),
            extension="png"
          )
        )
    return rendered_pages