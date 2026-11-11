if __name__ == "__main__" and not __package__:
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from docframework.core.rendered_page import RenderedPage
from docframework.core.pdf_document import PDFDocument
import pymupdf


class PDFPageRenderer:
    def render(self, document: PDFDocument, dpi: int = 150) -> list[RenderedPage]:
        rendered_pages: list[RenderedPage] = []

        with pymupdf.open(document.file_path) as doc:
            for index, page in enumerate(doc, start=1):
                render_page = page.get_pixmap(dpi=dpi)
                rendered_pages.append(
                    RenderedPage(
                        page_number=index,
                        image_bytes=render_page.tobytes("png"),
                        extension="png",
                    )
                )
        return rendered_pages


if __name__ == "__main__":
    import argparse

    from docframework.ingestion.pdf_loader import PDFLoader

    parser = argparse.ArgumentParser(
        description="Testa a renderização das páginas de um PDF."
    )
    parser.add_argument("pdf_path", help="Caminho para o arquivo PDF.")
    args = parser.parse_args()

    document = PDFLoader().load(args.pdf_path)
    rendered_pages = PDFPageRenderer().render(document)
    total_bytes = sum(len(page.image_bytes) for page in rendered_pages)
    print(f"Páginas renderizadas: {len(rendered_pages)}")
    print(f"Tamanho total das imagens: {total_bytes} bytes")
    print(rendered_pages)