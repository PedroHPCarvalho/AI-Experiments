from dataclasses import dataclass

@dataclass
class ExtractedImage:
  page_number: int
  image_index: int
  image_bytes: bytes
  extension: str