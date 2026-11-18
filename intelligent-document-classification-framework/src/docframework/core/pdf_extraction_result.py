from dataclasses import dataclass

from docframework.core.pdf_document import PDFDocument
from docframework.core.extraction_results import PageExtractionResult


@dataclass(frozen=True)
class PDFExtractionResult:
    document: PDFDocument
    pages: tuple[PageExtractionResult, ...]
