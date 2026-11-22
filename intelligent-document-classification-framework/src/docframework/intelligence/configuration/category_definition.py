from dataclasses import dataclass

@dataclass
class CategoryDefinition:
    name: str
    description: str
    criteria: list[str]
    exclusion_criteria: list[str]
    examples: list[str]