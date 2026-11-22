from abc import ABC, abstractmethod
from docframework.core.ai_request import AIRequest

class BaseProviderAI(ABC):

  @abstractmethod
  def generate_response(self,request_content: AIRequest) -> str:
    pass