from pydantic import BaseModel, ConfigDict, Field


class ClassificationEvidence(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        strict=True,
        str_strip_whitespace=True,
    )

    page_number: int = Field(ge=1)
    description: str = Field(min_length=1)


class ClassificationResult(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        strict=True,
        str_strip_whitespace=True,
    )

    document_type: str = Field(min_length=1)
    classification: str = Field(min_length=1)
    summary: str = Field(min_length=1)
    classification_reason: str = Field(min_length=1)
    evidence: list[ClassificationEvidence] = Field(min_length=1)