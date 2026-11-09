from pathlib import Path
import pymupdf

from docframework.core.pdf_document import PDFDocument
from .pdf_validator import PDFValidator


class PDFLoader:
    def __init__(self, max_size_mb: int = 10):
        self.validator = PDFValidator(max_size_mb=max_size_mb)

    def load(self, path_pdf: Path | str) -> PDFDocument:
        path_pdf = Path(path_pdf)

        # Validar o arquivo antes de abri-lo
        self.validator.validate(path=path_pdf)

        # Abrir o PDF e coletar seus metadados
        with pymupdf.open(path_pdf) as doc_loaded:
            pdf_obj = PDFDocument(
                file_path=path_pdf,
                filename=path_pdf.name,
                file_size_bytes=path_pdf.stat().st_size,
                page_count=doc_loaded.page_count
            )

        return pdf_obj