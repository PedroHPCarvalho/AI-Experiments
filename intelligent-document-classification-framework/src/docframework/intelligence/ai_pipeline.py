from docframework.intelligence.requests.ai_request_builder import AIRequest 
from docframework.intelligence.providers.base_provider_ai import BaseProviderAI  
from docframework.intelligence.response.response_parser import ResponseParser
from docframework.intelligence.response.response_validator import ResponseValidator


class AiPipeline:
  def __init__(self):
    pass
  def run_pipelineAI(self,request: AIRequest,provider: BaseProviderAI, response_parser: ResponseParser, response_validator: ResponseValidator) -> str:
    raw_response = provider.generate_response(request)
    parsed_response = response_parser.parse(raw_response=raw_response)
    validated_response = response_validator.validate(response=parsed_response)
    return validated_response
    