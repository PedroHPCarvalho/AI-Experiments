from docframework.intelligence.configuration.category_definition import CategoryDefinition
from docframework.intelligence.configuration.classification_config import ClassificationConfig


DEFAULT_CLASSIFICATION = ClassificationConfig(
    categories=[
        CategoryDefinition(
            name="Solicitação",
            description="O remetente solicita uma ação, alteração ou providência.",
            exclusion_criteria=[],
            criteria=[],
            examples=[]
        ),
        CategoryDefinition(
            name="Dúvida",
            description="O remetente busca esclarecimentos ou informações.",
            exclusion_criteria=[],
            criteria=[],
            examples=[]
        ),
        CategoryDefinition(
            name="Reclamação",
            description="O remetente manifesta insatisfação com um serviço ou processo.",
            exclusion_criteria=[],
            criteria=[],
            examples=[]
        ),
        CategoryDefinition(
            name="Contestação",
            description="O remetente questiona uma cobrança, transação ou decisão.",
            exclusion_criteria=[],
            criteria=[],
            examples=[]
        ),
        CategoryDefinition(
            name="Informativo",
            description="O documento comunica informações sem solicitar uma providência.",
            exclusion_criteria=[],
            criteria=[],
            examples=[]
        ),
        CategoryDefinition(
            name="Outros",
            description="O documento não se enquadra nas demais categorias ou não apresenta evidências suficientes.",
            exclusion_criteria=[],
            criteria=[],
            examples=[]
        )
    ]
)
