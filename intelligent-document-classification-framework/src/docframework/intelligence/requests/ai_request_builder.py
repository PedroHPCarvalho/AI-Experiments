# 1. Responsabilidade do AIRequestBuilder
# Ele será responsável por reunir três elementos:
# 1. Prompt: instruções carregadas pelo PromptManager.
# 2. Configuração: categorias e critérios fornecidos pelo ClassificationConfig.
# 3. Documento: conteúdo extraído pelo PDFExtractionPipeline.

from pathlib import Path
from docframework.intelligence.configuration.classification_config import ClassificationConfig
from docframework.intelligence.prompts.prompt_manager import PromptManager
from docframework.core.pdf_extraction_result import PDFExtractionResult
from docframework.core.ai_request import AIRequest


class AiRequestBuilder:
  def __init__(self, prompt_manager: PromptManager):
    self.prompt_manager = prompt_manager
  def build(
      self,
      template_name: str | Path, 
      results_extraction_document: PDFExtractionResult, 
      config_classification: ClassificationConfig
  ) -> AIRequest:
    system_prompt = self.prompt_manager.load_template(template_name)
    return AIRequest(
      system_prompt=system_prompt,
      classification_config=config_classification,
      content_extraction=results_extraction_document
    )
  

