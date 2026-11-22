import pymupdf

from docframework.core.extracted_page import ExtractedPage
from docframework.core.pdf_document import PDFDocument


class PDFTextExtractor:
    """Extracts the embedded text from a PDF, page by page.

    Uses PyMuPDF's `get_text()` method to read the text layer of each
    page. It does not use OCR (Tesseract), so it only works on PDFs
    that already contain selectable text. Scanned PDFs (images only)
    return empty text; use OCRExtractor for those.
    """

    def extract(self, document: PDFDocument) -> list[ExtractedPage]:
        """Extracts the text of every page in the document.

        Args:
            document: The PDFDocument to read, as returned by PDFLoader.

        Returns:
            One ExtractedPage per page, in order, with page numbers
            starting at 1.
        """
        extracted_pages: list[ExtractedPage] = []

        with pymupdf.open(document.file_path) as doc:
            # PyMuPDF pages are 0-indexed; start=1 gives human-friendly numbers
            for index, page in enumerate(doc, start=1):
                # Reads the embedded text layer directly, no OCR involved
                extracted_pages.append(
                    ExtractedPage(page_number=index, content_page=page.get_text())
                )

        return extracted_pages