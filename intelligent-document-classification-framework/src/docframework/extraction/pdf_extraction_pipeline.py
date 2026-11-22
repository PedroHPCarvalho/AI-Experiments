from docframework.core.extraction_results import PageExtractionResult
from docframework.core.pdf_document import PDFDocument
from docframework.core.pdf_extraction_result import PDFExtractionResult
from docframework.extraction.ocr_extractor import OCRExtractor
from docframework.extraction.pdf_image_extractor import PDFImageExtractor
from docframework.extraction.pdf_page_renderer import PDFPageRenderer
from docframework.extraction.pdf_text_extractor import PDFTextExtractor


class PDFExtractionPipeline:
    """Runs all the extraction steps on a PDF and consolidates the results.

    Steps, in order:
        1. Native text extraction (PDFTextExtractor)
        2. Embedded image extraction (PDFImageExtractor)
        3. Page rendering as images (PDFPageRenderer)
        4. OCR on the rendered pages (OCRExtractor), only if enabled

    The output of each step is indexed by page number, so the results
    can be combined into one PageExtractionResult per page.

    Attributes:
        enable_ocr: Whether the OCR step is enabled.
        ocr_extractor: The OCRExtractor, or None when OCR is disabled.
    """

    def __init__(self, enable_ocr: bool = False):
        """Initializes the pipeline and its extractors.

        Args:
            enable_ocr: If True, runs OCR on the rendered pages. It
                requires Tesseract to be installed and configured.

        Raises:
            EnvironmentError: If enable_ocr is True and Tesseract is
                not found (raised by OCRExtractor).
        """
        self.enable_ocr = enable_ocr
        self.text_native_extractor = PDFTextExtractor()
        self.image_extractor = PDFImageExtractor()
        self.page_render = PDFPageRenderer()

        # OCRExtractor checks for Tesseract when created, so it is only
        # instantiated when needed. This way the pipeline works without
        # Tesseract installed if OCR is disabled.
        self.ocr_extractor = OCRExtractor() if enable_ocr else None

    def run_pipeline(self, document: PDFDocument) -> PDFExtractionResult:
        """Runs all the steps and consolidates the results by page.

        Args:
            document: The PDFDocument to process, as returned by PDFLoader.

        Returns:
            A PDFExtractionResult with the document and one
            PageExtractionResult per page, in page order.
        """
        results_list: list[PageExtractionResult] = []

        text_native_list = self.text_native_extractor.extract(document)
        text_by_page = {page.page_number: page for page in text_native_list}

        # A page can have several images, so each key holds a list
        image_list = self.image_extractor.extract(document)
        image_by_page: dict[int, list] = {}
        for image in image_list:
            image_by_page.setdefault(image.page_number, []).append(image)

        rendered_list = self.page_render.render(document)
        render_by_page = {page.page_number: page for page in rendered_list}

        ocr_by_page = {}
        if self.ocr_extractor is not None:
            ocr_list = self.ocr_extractor.extract(rendered_list)
            ocr_by_page = {page.page_number: page for page in ocr_list}

        # Iterating by page number guarantees the final order, and .get()
        # returns None/empty for pages missing in any step
        for page_number in range(1, document.page_count + 1):
            results_list.append(
                PageExtractionResult(
                    page_number=page_number,
                    native_text=text_by_page.get(page_number),
                    images=tuple(image_by_page.get(page_number, [])),
                    rendered_page=render_by_page.get(page_number),
                    ocr_text=ocr_by_page.get(page_number),
                )
            )

        return PDFExtractionResult(document=document, pages=tuple(results_list))