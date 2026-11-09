import pymupdf
import pytest
from docframework.ingestion.pdf_loader import PDFLoader
from docframework.core.pdf_document import PDFDocument

def test_load_valid_pdf(tmp_path): 
  # Arrange: Criar um PDF real para teste
  pdf_path = tmp_path / "document.pdf"

  with pymupdf.open() as pdf:
    pdf.new_page()
    pdf.new_page()
    pdf.save(pdf_path)

  loader = PDFLoader(max_size_mb=10)
  result = loader.load(path_pdf=pdf_path)

  #Assert: verifiacr o resultado
  assert isinstance(result,PDFDocument)
  assert result.filename == "document.pdf"
  assert result.page_count == 2
  assert result.file_size_bytes == pdf_path.stat().st_size
  assert result.file_path == pdf_path


def test_format_invalid(tmp_path):
    file_path = tmp_path / "document.txt"
    file_path.write_text("conteudo de teste")

    loader = PDFLoader(max_size_mb=10)

    with pytest.raises(ValueError):
        loader.load(path_pdf=file_path)


def test_not_found(tmp_path):
    loader = PDFLoader(max_size_mb=10)

    with pytest.raises(FileNotFoundError):
        loader.load(path_pdf=tmp_path / "inexistente.pdf")


def test_corrupted_pdf(tmp_path):
    pdf_path = tmp_path / "corrupted.pdf"
    pdf_path.write_bytes(b"isso nao e um pdf valido")

    loader = PDFLoader(max_size_mb=10)

    with pytest.raises(Exception):
        loader.load(path_pdf=pdf_path)


def test_file_exceeds_size_limit(tmp_path):
    pdf_path = tmp_path / "large.pdf"
    pdf_path.write_bytes(b"conteudo de teste")

    loader = PDFLoader(max_size_mb=0)

    with pytest.raises(ValueError):
        loader.load(path_pdf=pdf_path)