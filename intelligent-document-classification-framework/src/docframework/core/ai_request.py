from dataclasses import dataclass
from docframework.intelligence.configuration.classification_config import ClassificationConfig
from docframework.core.pdf_extraction_result import PDFExtractionResult

@dataclass
class AIRequest:
  content_extraction: PDFExtractionResult
  classification_config : ClassificationConfig
  system_prompt: str
