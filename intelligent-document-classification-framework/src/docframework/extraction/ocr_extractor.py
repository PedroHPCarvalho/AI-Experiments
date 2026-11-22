import os
from io import BytesIO
from pathlib import Path

import pytesseract
from dotenv import load_dotenv
from PIL import Image

from docframework.core.extracted_page import ExtractedPage
from docframework.core.rendered_page import RenderedPage

load_dotenv(override=True)


class OCRExtractor:
    """Extracts text from rendered PDF pages using Tesseract OCR.

    Requires Tesseract to be installed, with its executable path set
    in the TESSERACT_CMD environment variable (or in a .env file).

    Attributes:
        languages: Tesseract language codes used in the recognition.
    """

    def __init__(self, languages: str = "por+eng"):
        """Initializes the extractor and locates the Tesseract executable.

        Args:
            languages: Tesseract language codes, joined by "+". The
                matching language data must be installed in Tesseract.

        Raises:
            EnvironmentError: If TESSERACT_CMD is not set or does not
                point to an existing file.
        """
        # Done here, not at import time, so that importing the module
        # does not fail on machines without Tesseract configured
        tesseract_path = os.getenv("TESSERACT_CMD")

        if not tesseract_path or not Path(tesseract_path).is_file():
            raise EnvironmentError(
                "Tesseract not found. Check the TESSERACT_CMD variable."
            )

        pytesseract.pytesseract.tesseract_cmd = tesseract_path
        self.languages = languages

    def extract(self, rendered_pages: list[RenderedPage]) -> list[ExtractedPage]:
        """Runs OCR on each rendered page.

        Args:
            rendered_pages: Pages already rendered as images.

        Returns:
            One ExtractedPage per input page, in the same order, with
            the recognized text.
        """
        extracted_pages: list[ExtractedPage] = []

        for rendered_page in rendered_pages:
            # Image.open is lazy; the `with` ensures the buffer is
            # released after each page, keeping memory usage low
            with Image.open(BytesIO(rendered_page.image_bytes)) as image:
                image.load()
                text = pytesseract.image_to_string(image, lang=self.languages)

            extracted_pages.append(
                ExtractedPage(
                    page_number=rendered_page.page_number,
                    content_page=text,
                )
            )

        return extracted_pages