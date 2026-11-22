import base64
import json
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock

import pytest

from docframework.core.ai_request import AIRequest
from docframework.core.category_definition import CategoryDefinition
from docframework.core.extracted_image import ExtractedImage
from docframework.core.extracted_page import ExtractedPage
from docframework.core.extraction_results import PageExtractionResult
from docframework.core.pdf_document import PDFDocument
from docframework.core.pdf_extraction_result import PDFExtractionResult
from docframework.core.rendered_page import RenderedPage
from docframework.intelligence.configuration.classification_config import (
    ClassificationConfig,
)
from docframework.intelligence.providers.gemini_provider_api import (
    GeminiProviderAPI,
)
from docframework.intelligence.response.response_parser import ResponseParser
from docframework.intelligence.response.response_validator import ResponseValidator


class TestGeminiProviderAPI:
    @pytest.fixture
    def provider(self, monkeypatch):
        response_text = json.dumps(
            {
                "document_type": "Currículo profissional",
                "classification": "curriculo",
                "summary": "Documento fictício de currículo.",
                "classification_reason": "Apresenta experiência e competências profissionais.",
                "evidence": [
                    {
                        "page_number": 1,
                        "description": "O texto descreve experiência profissional.",
                    }
                ],
            }
        )
        client = SimpleNamespace(
            interactions=SimpleNamespace(
                create=Mock(
                    return_value=SimpleNamespace(output_text=response_text)
                )
            )
        )
        monkeypatch.setattr(
            "docframework.intelligence.providers.gemini_provider_api.genai.Client",
            lambda **kwargs: client,
        )
        return GeminiProviderAPI(api_key="test-api-key")

    @staticmethod
    def make_request(pages):
        return AIRequest(
            content_extraction=PDFExtractionResult(
                document=PDFDocument(
                    file_path=Path("example.pdf"),
                    filename="example.pdf",
                    file_size_bytes=100,
                    page_count=len(pages),
                ),
                pages=tuple(pages),
            ),
            classification_config=ClassificationConfig(
                categories=[
                    CategoryDefinition(
                        name="curriculo",
                        description="Um currículo profissional.",
                        criteria=["Apresenta experiência e competências profissionais."],
                        exclusion_criteria=[],
                        examples=[],
                    ),
                    CategoryDefinition(
                        name="outro",
                        description="Documento diferente de um currículo.",
                        criteria=["Não atende aos critérios de currículo."],
                        exclusion_criteria=[],
                        examples=[],
                    )
                ]
            ),
            system_prompt="Classify the document.",
        )

    def test_build_input_includes_page_text_and_normalizes_empty_ocr(self, provider):
        request = self.make_request(
            [
                PageExtractionResult(
                    page_number=1,
                    native_text=ExtractedPage(1, "Native text"),
                    ocr_text=ExtractedPage(1, ""),
                    images=(),
                )
            ]
        )

        assert provider.build_input(request) == [
            {
                "page_number": 1,
                "native_text": "Native text",
                "ocr_text": None,
                "images": [],
            }
        ]

    def test_build_input_encodes_extracted_and_rendered_images(self, provider):
        extracted_bytes = b"extracted-image"
        rendered_bytes = b"rendered-image"
        request = self.make_request(
            [
                PageExtractionResult(
                    page_number=2,
                    native_text=None,
                    ocr_text=ExtractedPage(2, "OCR text"),
                    images=(
                        ExtractedImage(
                            page_number=2,
                            image_index=3,
                            image_bytes=extracted_bytes,
                            extension=".PNG",
                        ),
                    ),
                    rendered_page=RenderedPage(
                        page_number=2,
                        image_bytes=rendered_bytes,
                        extension="jpg",
                    ),
                )
            ]
        )

        assert provider.build_input(request) == [
            {
                "page_number": 2,
                "native_text": None,
                "ocr_text": "OCR text",
                "images": [
                    {
                        "page_number": 2,
                        "image_index": 3,
                        "source": "extracted_image",
                        "mime_type": "image/png",
                        "data": base64.b64encode(extracted_bytes).decode("utf-8"),
                    },
                    {
                        "page_number": 2,
                        "image_index": None,
                        "source": "rendered_page",
                        "mime_type": "image/jpeg",
                        "data": base64.b64encode(rendered_bytes).decode("utf-8"),
                    },
                ],
            }
        ]

    def test_build_input_rejects_unsupported_image_format(self, provider):
        request = self.make_request(
            [
                PageExtractionResult(
                    page_number=1,
                    native_text=None,
                    ocr_text=None,
                    images=(
                        ExtractedImage(
                            page_number=1,
                            image_index=0,
                            image_bytes=b"image",
                            extension="bmp",
                        ),
                    ),
                )
            ]
        )

        with pytest.raises(ValueError, match="Unsupported image format: bmp"):
            provider.build_input(request)

    def test_generate_response_prints_built_input(self, provider, capsys):
        request = self.make_request(
            [
                PageExtractionResult(
                    page_number=1,
                    native_text=ExtractedPage(1, "Resume content"),
                    ocr_text=None,
                    images=(),
                )
            ]
        )

        response = provider.generate_response(request)

        printed_input = capsys.readouterr().out
        assert json.loads(printed_input) == [
            {
                "type": "text",
                "text": "Conteúdo da página 1\n\nTexto nativo:\nResume content",
            }
        ]
        print(printed_input, end="")
        parsed_response = ResponseParser().parse(response)
        result = ResponseValidator().validate(parsed_response)
        assert result.classification == "curriculo"
        assert result.evidence[0].page_number == 1
        provider.client.interactions.create.assert_called_once()
        call = provider.client.interactions.create.call_args.kwargs
        assert call["model"] == "gemini-2.5-flash"
        assert "curriculo" in call["system_instruction"]
        assert call["input"] == json.loads(printed_input)

    def test_generate_response_prints_empty_input(self, provider, capsys):
        request = self.make_request([])

        with pytest.raises(ValueError, match="No content found to send to Gemini"):
            provider.generate_response(request)

        assert json.loads(capsys.readouterr().out) == []
        provider.client.interactions.create.assert_not_called()
