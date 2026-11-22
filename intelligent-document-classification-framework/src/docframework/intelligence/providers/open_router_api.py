
import base64
import json
import mimetypes

from openai import OpenAI

from docframework.core.ai_request import AIRequest
from docframework.intelligence.providers.base_provider_ai import BaseProviderAI


class OpenRouterProviderAPI(BaseProviderAI):

    def __init__(
        self,
        api_key: str,
        model: str = "nvidia/nemotron-3.5-super-vl:free"
    ):
        self.client = OpenAI(
            api_key=api_key,
            base_url="https://openrouter.ai/api/v1"
        )
        self.model = model

    def build_system_instruction(self, ai_request: AIRequest) -> str:
        categories = ai_request.classification_config.model_dump()

        return (
            f"{ai_request.system_prompt}\n\n"
            "Categorias disponíveis para classificação:\n"
            f"{json.dumps(categories, ensure_ascii=False, indent=2)}"
        )

    def encode_image(self, image_bytes: bytes, extension: str) -> str:
        extension = extension.lower().lstrip(".")

        mime_type = mimetypes.guess_type(
            f"image.{extension}"
        )[0] or "image/png"

        encoded_image = base64.b64encode(
            image_bytes
        ).decode("utf-8")

        return f"data:{mime_type};base64,{encoded_image}"

    def build_input(self, ai_request: AIRequest) -> list[dict]:
        content = []

        extraction = ai_request.content_extraction

        for page in extraction.pages:
            content.append({
                "type": "text",
                "text": f"\n--- Página {page.page_number} ---"
            })

            if page.native_text:
                content.append({
                    "type": "text",
                    "text": (
                        "[Texto nativo]\n"
                        f"{page.native_text.content_page}"
                    )
                })

            if page.ocr_text:
                content.append({
                    "type": "text",
                    "text": (
                        "[Texto OCR]\n"
                        f"{page.ocr_text.content_page}"
                    )
                })

            images = list(page.images)

            if page.rendered_page:
                images.append(page.rendered_page)

            for image in images:
                image_url = self.encode_image(
                    image.image_bytes,
                    image.extension
                )

                content.append({
                    "type": "image_url",
                    "image_url": {
                        "url": image_url
                    }
                })

        return content

    def generate_response(self, request_content: AIRequest) -> str:
        system_instruction = self.build_system_instruction(
            request_content
        )

        user_content = self.build_input(request_content)

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": system_instruction
                },
                {
                    "role": "user",
                    "content": user_content
                }
            ],
            response_format={
                "type": "json_object"
            },
            temperature=0.1,
            max_tokens=4096
        )

        result = response.choices[0].message.content

        if not result:
            raise ValueError(
                "OpenRouter retornou uma resposta vazia."
            )

        return result
