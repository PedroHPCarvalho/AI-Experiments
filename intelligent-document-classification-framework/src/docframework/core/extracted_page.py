from dataclasses import dataclass

@dataclass(frozen=True)
class ExtractedPage:
  page_number: int
  content_page: str