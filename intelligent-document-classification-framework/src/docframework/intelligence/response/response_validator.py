from docframework.core.classification_result import ClassificationResult


class ResponseValidator:
    def validate(self, response: object) -> ClassificationResult:
        return ClassificationResult.model_validate(response, strict=True)
