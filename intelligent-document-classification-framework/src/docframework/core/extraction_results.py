from dataclasses import dataclass
from docframework.core.extracted_image import ExtractedImage
from docframework.core.extracted_page import ExtractedPage 
from docframework.core.rendered_page import RenderedPage

@dataclass(frozen=True)
class PageExtractionResult:
    page_number: int
    native_text: ExtractedPage | None
    ocr_text: ExtractedPage | None
    images: tuple[ExtractedImage, ...]
    rendered_page: RenderedPage | None = None