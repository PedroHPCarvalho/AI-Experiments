import json
from typing import Any


class ResponseParser:
    def parse(self, raw_response: str) -> Any:
        if not isinstance(raw_response, str):
            raise TypeError("A resposta bruta deve ser uma string.")

        try:
            return json.loads(raw_response)
        except json.JSONDecodeError as exc:
            raise ValueError(
                f"Resposta inválida: conteúdo não é um JSON válido "
                f"(linha {exc.lineno}, coluna {exc.colno})."
            ) from exc
