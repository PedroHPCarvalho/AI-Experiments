from pydantic import BaseModel, Field, model_validator
from docframework.core.category_definition import CategoryDefinition

class ClassificationConfig(BaseModel):
  categories: list[CategoryDefinition] = Field(min_length=1)

  @model_validator(mode="after")
  def validate_unique_categories(self):
    names = [category.name.strip().lower() for category in self.categories]

    if len(names) != len(set(names)):
      raise ValueError("Category names must be unique.")

    return self