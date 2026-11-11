if __name__ == "__main__" and not __package__:
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from docframework.core.pdf_document import PDFDocument
from docframework.core.extracted_page import ExtractedPage
import pymupdf


class PDFTextExtractor:
    def extract(self, document: PDFDocument) -> list[ExtractedPage]:
        extracted_pages: list[ExtractedPage] = []

        with pymupdf.open(document.file_path) as doc:
            for index, page in enumerate(doc, start=1):
                extracted_pages.append(
                    ExtractedPage(page_number=index, content_page=page.get_text())
                )

        return extracted_pages


if __name__ == "__main__":
    import argparse
    import pprint

    from docframework.ingestion.pdf_loader import PDFLoader

    parser = argparse.ArgumentParser(description="Testa a extração de texto de um PDF.")
    parser.add_argument("pdf_path", help="Caminho para o arquivo PDF.")
    args = parser.parse_args()

    document = PDFLoader().load(args.pdf_path)
    pages = PDFTextExtractor().extract(document)
    total_characters = sum(len(page.content_page) for page in pages)
    print(f"Páginas processadas: {len(pages)}")
    print(f"Caracteres extraídos: {total_characters}")
    pprint.pprint(pages)