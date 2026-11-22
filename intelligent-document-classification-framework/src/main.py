import pprint
from docframework.extraction.pdf_extraction_pipeline import PDFExtractionPipeline
from docframework.ingestion.pdf_loader import PDFLoader
from docframework.intelligence.configuration.default_categories import DEFAULT_CLASSIFICATION
from docframework.intelligence.requests.ai_request_builder import AiRequestBuilder
from docframework.intelligence.providers.gemini_provider_api import GeminiProviderAPI
from docframework.intelligence.providers.open_router_api import OpenRouterProviderAPI
from docframework.intelligence.response.response_validator import ResponseValidator 
from docframework.intelligence.response.response_parser import ResponseParser  
from docframework.intelligence.ai_pipeline import AiPipeline
import os
from dotenv import load_dotenv
load_dotenv()
from pathlib import Path


def main():
    # 1. Receber o PDF
    file_path = Path(r"C:\Users\pedro\Documents\AI-Experiments\intelligent-document-classification-framework\mock_docs\03_comunicacao_sinistro_com_imagem.pdf")
    loader_pdf = PDFLoader(max_size_mb=60)
    pdf_loaded = loader_pdf.load(path_pdf=file_path)

    # 2. Executar a extração
    pipeline_extract = PDFExtractionPipeline(enable_ocr=True)
    content_extracted = pipeline_extract.run_pipeline(document=pdf_loaded)

    # 3. Carregar o prompt e as categorias
    categories = DEFAULT_CLASSIFICATION

    # 4. Construir AIRequest
    template_path = Path(r"C:\Users\pedro\Documents\AI-Experiments\intelligent-document-classification-framework\src\docframework\intelligence\prompts\templates")
    builder_request = AiRequestBuilder(templates_dir=template_path)
    request = builder_request.build(
        template_name="document_classification.md",
        config_classification=DEFAULT_CLASSIFICATION,
        results_extraction_document=content_extracted,
    )

    # 5. Instanciar o provider
    # gemini_provider = GeminiProviderAPI(
    #     api_key= os.getenv("GEMINI_API_KEY"),
    #     model="gemini-4-hydrogen"
    # )
    openrouter= OpenRouterProviderAPI(
        api_key= os.getenv("OPEN_ROUTER_KEY"),
        model="nvidia/nemotron-3.5-super-vl:free"
    )

    # 6. Instanciar parser e validator
    validator = ResponseValidator()
    parser =ResponseParser()

    # 7. Executar AIPipeline
    pipeline_ai = AiPipeline()
    response = pipeline_ai.run_pipelineAI(
        request=request,
        provider=openrouter,
        response_parser=parser,
        response_validator=validator,
    )
    # 8. Exibir resultado
    # print(response)
    # pprint(response)
    # 9. salvar teste 
    import json
    output_path = Path("outputs/classification_result4.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as file:
        json.dump(
            response.model_dump(),
            file,
            ensure_ascii=False,
            indent=4
        )


if __name__ == "__main__":
    main()