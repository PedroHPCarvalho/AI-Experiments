import pytest
from docframework.ingestion.pdf_validator import PDFValidator


def test_validate_valid_pdf(tmp_path):
  pdf_file = tmp_path/ "document.pdf"
  pdf_file.write_bytes(b"conteudo de teste")

  validator = PDFValidator(max_size_mb=10)
  validator.validate(path=pdf_file)


def test_validate_valid_pdf_upper(tmp_path):
  pdf_file = tmp_path/ "document.PDF"
  pdf_file.write_bytes(b"conteudo de teste")

  validator = PDFValidator(max_size_mb=10)
  validator.validate(path=pdf_file)


def test_validate_file_not_found(tmp_path):
  validator =  PDFValidator(max_size_mb=10)

  with pytest.raises(FileNotFoundError):
    validator.validate(path=tmp_path / "inexistente.pdf")


def test_format_valid(tmp_path):
  validator = PDFValidator(max_size_mb=10)
  archive_test = tmp_path / "formato_errado.txt"
  archive_test.write_text("conteudo de teste")

  with pytest.raises(ValueError):
    validator.validate(path=tmp_path / "formato_errado.txt")


def test_limit_mb(tmp_path):
  validator = PDFValidator(max_size_mb=0)
  archive_test = tmp_path / "limite_teste.pdf"
  archive_test.write_text("conteudo de teste")

  with pytest.raises(ValueError):
    validator.validate(path=tmp_path / "limite_teste.pdf")