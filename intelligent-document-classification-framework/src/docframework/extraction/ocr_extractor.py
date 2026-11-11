
from docframework.core.rendered_page import RenderedPage
from docframework.core.extracted_page import ExtractedPage

from io import BytesIO
from PIL import Image
import pytesseract


class OCRExtractor:
    def __init__(self, languages: str = "por+eng"):
        self.languages = languages

    def extract(
        self, rendered_pages: list[RenderedPage]
    ) -> list[ExtractedPage]:

        extracted_pages: list[ExtractedPage] = []

        for rendered_page in rendered_pages:
            with Image.open(BytesIO(rendered_page.image_bytes)) as image:
                image.load()
                text = pytesseract.image_to_string(
                    image, lang=self.languages
                )

            extracted_pages.append(
                ExtractedPage(
                    page_number=rendered_page.page_number,
                    content_page=text
                )
            )

        return extracted_pages
