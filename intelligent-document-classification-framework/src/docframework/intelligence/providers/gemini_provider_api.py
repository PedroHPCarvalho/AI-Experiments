from docframework.core.ai_request import AIRequest
from docframework.core.extraction_results import PageExtractionResult
from docframework.intelligence.providers.base_provider_ai import BaseProviderAI
import base64
from google import genai
from dotenv import load_dotenv
import os
import json

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

class GeminiProviderAPI(BaseProviderAI):
    def __init__(self, api_key: str, model: str = "gemini-2.5-flash"):
        self.client = genai.Client(api_key=api_key)
        self.model = model

    def build_system_instruction(self, ai_request: AIRequest) -> dict:
        instructions = {
            "system_prompt": ai_request.system_prompt,
            "categories": ai_request.classification_config.model_dump()
        }
        return instructions

    def collect_images(self, page: PageExtractionResult) -> list[dict]:
        images = []

        for image in page.images:
            images.append({
                "page_number": page.page_number,
                "image_index": image.image_index,
                "image_bytes": image.image_bytes,
                "extension": image.extension,
                "source": "extracted_image"
            })

        if page.rendered_page is not None:
            images.append({
                "page_number": page.page_number,
                "image_index": None,
                "image_bytes": page.rendered_page.image_bytes,
                "extension": page.rendered_page.extension,
                "source": "rendered_page"
            })

        return images

    def encode_image(self, image: dict) -> dict:
        extension = image["extension"].lower().lstrip(".")

        mime_types = {
            "png": "image/png",
            "jpg": "image/jpeg",
            "jpeg": "image/jpeg",
            "webp": "image/webp",
        }

        mime_type = mime_types.get(extension)

        if mime_type is None:
            raise ValueError(f"Unsupported image format: {extension}")

        encoded_image = base64.b64encode(
            image["image_bytes"]
        ).decode("utf-8")

        return {
            "page_number": image["page_number"],
            "image_index": image["image_index"],
            "source": image["source"],
            "mime_type": mime_type,
            "data": encoded_image
        }

    def build_input(self, ai_request: AIRequest) -> list[dict]:
        content_input = []

        for page in ai_request.content_extraction.pages:
            page_content = {
                "page_number": page.page_number,
                "native_text": (
                    page.native_text.content_page
                    if page.native_text else None
                ),
                "ocr_text": (
                    page.ocr_text.content_page
                    if page.ocr_text and page.ocr_text.content_page
                    else None
                ),
                "images": []
            }

            # Imagens incorporadas e páginas renderizadas
            images = self.collect_images(page)

            for image in images:
                page_content["images"].append(
                    self.encode_image(image)
                )

            content_input.append(page_content)

        return content_input
    
    def generate_response(self, request_content: AIRequest) -> str:

      # 1. Preparar as instruções
      instructions = self.build_system_instruction(request_content)

      system_instruction = (
          f"{instructions['system_prompt']}\n\n"
          "Categorias disponíveis para classificação:\n"
          f"{json.dumps(instructions['categories'], ensure_ascii=False, indent=2)}"
      )

      # 2. Preparar o conteúdo extraído
      pages = self.build_input(request_content)

      # 3. Converter nossa estrutura intermediária
      # para o formato multimodal do Gemini
      gemini_input = []

      for page in pages:

          page_text = [f"Conteúdo da página {page['page_number']}"]

          if page["native_text"]:
              page_text.append(
                  f"Texto nativo:\n{page['native_text']}"
              )

          if page["ocr_text"]:
              page_text.append(
                  f"Texto OCR:\n{page['ocr_text']}"
              )

          if len(page_text) > 1:
              gemini_input.append({
                  "type": "text",
                  "text": "\n\n".join(page_text)
              })

          for image in page["images"]:

              gemini_input.append({
                  "type": "text",
                  "text": (
                      f"Imagem da página {image['page_number']}. "
                      f"Origem: {image['source']}."
                  )
              })

              gemini_input.append({
                  "type": "image",
                  "data": image["data"],
                  "mime_type": image["mime_type"]
              })

    #   print(json.dumps(gemini_input, ensure_ascii=False, indent=2))

      if not gemini_input:
          raise ValueError("No content found to send to Gemini.")

      # 4. Enviar requisição
      interaction = self.client.interactions.create(
          model=self.model,
          system_instruction=system_instruction,
          input=gemini_input
      )

      # 5. Retornar resposta textual
      return interaction.output_text

