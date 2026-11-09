from docframework.core.rendered_page import RenderedPage
from docframework.core.extracted_page import ExtractedPage
from io import BytesIO
from PIL import Image
import pytesseract

class OCRExtractor:
  def __init__(self, languages: str = "por+eng"):
    self.languages=languages

  def extract(self, rendered_page: RenderedPage) -> ExtractedPage:
    with Image.open(BytesIO(rendered_page.image_bytes)) as image:
      image.load()
      text = pytesseract.image_to_string(
        image,
        lang=self.languages
      )
    return ExtractedPage(page_number=rendered_page.page_number,content_page=text)
      