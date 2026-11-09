from dataclasses import dataclass

@dataclass
class RenderedPage:
  page_number: int
  image_bytes: bytes
  extension: str