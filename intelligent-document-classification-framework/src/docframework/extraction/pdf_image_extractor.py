if __name__ == "__main__" and not __package__:
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from docframework.core.pdf_document import PDFDocument
from docframework.core.extracted_image import ExtractedImage
import pymupdf


class PDFImageExtractor:
    def extract(self, document: PDFDocument) -> list[ExtractedImage]:
        extracted_images: list[ExtractedImage] = []

        with pymupdf.open(document.file_path) as doc:
            for index, page in enumerate(doc, start=1):
                for image_index, image_info in enumerate(
                    page.get_images(full=True), start=1
                ):
                    xref = image_info[0]
                    image_data = doc.extract_image(xref)
                    extracted_images.append(
                        ExtractedImage(
                            page_number=index,
                            image_index=image_index,
                            image_bytes=image_data["image"],
                            extension=image_data["ext"],
                        )
                    )

        return extracted_images

if __name__ == "__main__":
    import argparse

    from docframework.ingestion.pdf_loader import PDFLoader

    parser = argparse.ArgumentParser(
        description="Testa a extração de imagens de um PDF."
    )
    parser.add_argument("pdf_path", help="Caminho para o arquivo PDF.")
    args = parser.parse_args()

    document = PDFLoader().load(args.pdf_path)
    images = PDFImageExtractor().extract(document)
    print(f"Imagens extraídas: {len(images)}")
    print(images)
