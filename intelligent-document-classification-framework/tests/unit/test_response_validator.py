import pytest
from pydantic import ValidationError

from docframework.core.classification_result import (
    ClassificationEvidence,
    ClassificationResult,
)
from docframework.intelligence.response.response_validator import ResponseValidator


@pytest.fixture
def valid_response():
    return {
        "document_type": "E-mail corporativo",
        "classification": "Solicitação de ajuste cadastral",
        "summary": "Resumo do documento.",
        "classification_reason": "Justificativa da classificação.",
        "evidence": [
            {
                "page_number": 1,
                "description": "Evidência encontrada na página.",
            }
        ],
    }


def test_validate_returns_typed_classification(valid_response):
    result = ResponseValidator().validate(valid_response)

    assert isinstance(result, ClassificationResult)
    assert isinstance(result.evidence[0], ClassificationEvidence)
    assert result.document_type == "E-mail corporativo"
    assert result.evidence[0].page_number == 1


def test_validate_rejects_missing_required_field(valid_response):
    del valid_response["classification_reason"]

    with pytest.raises(ValidationError, match="classification_reason"):
        ResponseValidator().validate(valid_response)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("document_type", 123),
        ("classification", None),
        ("summary", ""),
        ("classification_reason", "   "),
        ("evidence", "Evidência encontrada na página."),
    ],
)
def test_validate_rejects_invalid_field_types_and_empty_values(
    valid_response, field, value
):
    valid_response[field] = value

    with pytest.raises(ValidationError):
        ResponseValidator().validate(valid_response)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("page_number", "1"),
        ("page_number", 0),
        ("description", ""),
    ],
)
def test_validate_rejects_invalid_nested_evidence(valid_response, field, value):
    valid_response["evidence"][0][field] = value

    with pytest.raises(ValidationError):
        ResponseValidator().validate(valid_response)


def test_validate_rejects_empty_evidence_list(valid_response):
    valid_response["evidence"] = []

    with pytest.raises(ValidationError, match="at least 1 item"):
        ResponseValidator().validate(valid_response)


def test_validate_rejects_unexpected_fields(valid_response):
    valid_response["extra"] = "não esperado"

    with pytest.raises(ValidationError, match="extra"):
        ResponseValidator().validate(valid_response)


@pytest.mark.parametrize("response", [None, [], "not an object"])
def test_validate_rejects_non_object_response(response):
    with pytest.raises(ValidationError):
        ResponseValidator().validate(response)
