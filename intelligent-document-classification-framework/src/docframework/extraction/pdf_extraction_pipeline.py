if __name__ == "__main__" and not __package__:
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from docframework.core.pdf_document import PDFDocument
from docframework.core.extraction_results import PageExtractionResult
from docframework.extraction.pdf_text_extractor import PDFTextExtractor
from docframework.extraction.pdf_image_extractor import PDFImageExtractor 
from docframework.extraction.pdf_page_renderer import PDFPageRenderer 
from docframework.extraction.ocr_extractor import OCRExtractor 

class PDFExtractionPipeline:
  def __init__(self, enable_ocr: bool = False):
    self.enable_ocr = enable_ocr
    self.text_native_extractor = PDFTextExtractor()
    self.image_extractor = PDFImageExtractor()
    self.page_render = PDFPageRenderer()
    if enable_ocr != False:
      self.ocr_extractor = OCRExtractor()
    else:
      self.ocr_extractor = None

  def run_pipeline(self, document: PDFDocument) ->list[PageExtractionResult]:
    results_list: list[PageExtractionResult]= []

    text_native_list = self.text_native_extractor.extract(document)
    text_by_page = {
      page.page_number: page
      for page in text_native_list
    }

    image_list = self.image_extractor.extract(document)
    image_by_page = {}
    for image in image_list:
      image_by_page.setdefault(image.page_number, []).append(image)

    rendered_list = self.page_render.render(document)
    render_by_page = {
      page.page_number: page
      for page in rendered_list
    }

    ocr_by_page = {}

    if self.ocr_extractor is not None:
        ocr_list = self.ocr_extractor.extract(rendered_list)

        ocr_by_page = {
            page.page_number: page
            for page in ocr_list
        }

    for page_number in range(1,document.page_count + 1):
      results_list.append(
        PageExtractionResult(
          page_number=page_number,
          native_text=text_by_page.get(page_number),
          images=tuple(image_by_page.get(page_number, [])),
          rendered_page=render_by_page.get(page_number),
          ocr_text=ocr_by_page.get(page_number)
        )
      )

    return results_list

if __name__ == "__main__":
    import argparse
    import pprint

    from docframework.ingestion.pdf_loader import PDFLoader

    parser = argparse.ArgumentParser(
        description="Executa o pipeline de extração de um PDF."
    )
    parser.add_argument("pdf_path", help="Caminho para o arquivo PDF.")
    args = parser.parse_args()
    document = PDFLoader().load(args.pdf_path)
    result_extract = PDFExtractionPipeline(enable_ocr=True).run_pipeline(document)
    native_characters = sum(
        len(result.native_text.content_page)
        for result in result_extract
        if result.native_text is not None
    )
    ocr_characters = sum(
        len(result.ocr_text.content_page)
        for result in result_extract
        if result.ocr_text is not None
    )
    image_count = sum(len(result.images) for result in result_extract)

    print(f"Páginas processadas: {len(result_extract)}")
    print(f"Imagens extraídas: {image_count}")
    print(f"Caracteres extraídos do texto nativo: {native_characters}")
    print(f"Caracteres reconhecidos por OCR: {ocr_characters}")
    print()
    pprint.pprint(result_extract[0].page_number)
    print()
    pprint.pprint(result_extract[0].native_text)
    print()
    pprint.pprint(result_extract[0].images)
    print()
    pprint.pprint(result_extract[0].rendered_page)
    print()
    pprint.pprint(result_extract[0].ocr_text)

