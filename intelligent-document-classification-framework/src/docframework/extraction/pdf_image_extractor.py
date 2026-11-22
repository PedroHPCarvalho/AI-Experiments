import pymupdf

from docframework.core.extracted_image import ExtractedImage
from docframework.core.pdf_document import PDFDocument


class PDFImageExtractor:
    """Extracts the images embedded in a PDF, page by page.

    Loops over the pages, lists the images of each one with
    PyMuPDF's `get_images()` and reads each image's data using its
    xref (the internal reference number PyMuPDF uses to identify
    objects in the PDF).

    Only extracts images stored as separate objects in the PDF. It does
    not render pages, so text and vector graphics are not included.
    """

    def extract(self, document: PDFDocument) -> list[ExtractedImage]:
        """Extracts all embedded images of the document.

        Args:
            document: The PDFDocument to read, as returned by PDFLoader.

        Returns:
            A list of ExtractedImage, in page order, each with its page
            number, its position in the page (starting at 1), the raw
            image bytes and the file extension (e.g. "png", "jpeg").
        """
        extracted_images: list[ExtractedImage] = []

        with pymupdf.open(document.file_path) as doc:
            for index, page in enumerate(doc, start=1):
                # full=True includes extra info per image (e.g. the
                # soft mask), and the xref is always the first item
                for image_index, image_info in enumerate(
                    page.get_images(full=True), start=1
                ):
                    xref = image_info[0]

                    # The xref identifies the image object in the PDF;
                    # the same image can appear on several pages
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