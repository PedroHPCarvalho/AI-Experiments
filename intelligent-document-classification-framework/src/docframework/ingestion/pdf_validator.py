from pathlib import Path

class PDFValidator:
    def __init__(self, max_size_mb: int = 50):
        self.max_size_bytes = max_size_mb * 1024 * 1024

    def validate(self, path: Path | str) -> None:
            if not path.exists():
                raise FileNotFoundError(f"Arquivo não encontrado: {path}")
            if path.suffix.lower() != ".pdf":
                raise ValueError(f"Arquivo encontrado fora de formato PDF: {path}")
            if path.stat().st_size > self.max_size_bytes :
                raise ValueError(f"Arquivo encontrado ultrapassa o limite de Tamaho: {path}")

          
          