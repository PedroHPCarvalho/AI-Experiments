from pathlib import Path

import pymupdf

from docframework.core.pdf_document import PDFDocument

from .pdf_validator import PDFValidator


class PDFLoader:
    """Loads PDF files and returns a PDFDocument with their metadata.

    Validates the file before opening it, so only valid PDFs within
    the size limit reach the next stages.

    Attributes:
        validator: Validator used to check each file before loading.
    """

    def __init__(self, max_size_mb: int = 10):
        """Initializes the loader.

        Args:
            max_size_mb: Maximum allowed PDF size, in megabytes.
        """
        self.validator = PDFValidator(max_size_mb=max_size_mb)

    def load(self, path_pdf: Path | str) -> PDFDocument:
        """Loads a PDF and extracts its metadata.

        Args:
            path_pdf: Path to the PDF file, as a Path or a string.

        Returns:
            A PDFDocument with the file path, name, size in bytes
            and page count.

        Raises:
            FileNotFoundError: If the file does not exist.
            PDFValidationError: If the file fails validation.
        """
        # Accept both str and Path, but work with Path from here on
        path_pdf = Path(path_pdf)

        # Validate before opening: avoids loading a corrupted or
        # oversized file into memory
        self.validator.validate(path=path_pdf)

        # The object is built inside the `with` because page_count
        # requires the document to be open
        with pymupdf.open(path_pdf) as doc_loaded:
            pdf_obj = PDFDocument(
                file_path=path_pdf,
                filename=path_pdf.name,
                file_size_bytes=path_pdf.stat().st_size,
                page_count=doc_loaded.page_count,
            )

        return pdf_obj