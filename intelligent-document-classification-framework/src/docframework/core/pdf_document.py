from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class PDFDocument:
    file_path: Path
    filename: str
    file_size_bytes: int
    page_count: int
