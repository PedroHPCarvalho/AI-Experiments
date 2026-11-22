import pymupdf

from docframework.core.pdf_document import PDFDocument
from docframework.core.rendered_page import RenderedPage


class PDFPageRenderer:
    """Renders each PDF page as an image.

    Uses PyMuPDF's `get_pixmap()` method to draw the full page (text,
    images and vector graphics) as a PNG. The result is useful for
    scanned PDFs and as input for OCRExtractor or for AI models that
    read images.

    Unlike PDFImageExtractor, which returns only the images embedded
    in the PDF, this class returns the whole page as it looks on screen.
    """

    def render(self, document: PDFDocument, dpi: int = 150) -> list[RenderedPage]:
        """Renders every page of the document as a PNG image.

        Args:
            document: The PDFDocument to render, as returned by PDFLoader.
            dpi: Resolution of the output images. Higher values give
                better quality (and better OCR), but use more memory.

        Returns:
            One RenderedPage per page, in order, with page numbers
            starting at 1.
        """
        rendered_pages: list[RenderedPage] = []

        with pymupdf.open(document.file_path) as doc:
            for index, page in enumerate(doc, start=1):
                # The pixmap is PyMuPDF's raster image of the page;
                # it is converted to PNG bytes right away so no
                # PyMuPDF object is kept in memory
                pixmap = page.get_pixmap(dpi=dpi)

                rendered_pages.append(
                    RenderedPage(
                        page_number=index,
                        image_bytes=pixmap.tobytes("png"),
                        extension="png",
                    )
                )

        return rendered_pages