from pathlib import Path


class PDFValidator:
    """Validates a PDF file before it is loaded.

    Checks that the file exists, has a .pdf extension and does not
    exceed the maximum allowed size.

    Attributes:
        max_size_bytes: Maximum allowed file size, in bytes.
    """

    def __init__(self, max_size_mb: int = 50):
        """Initializes the validator.

        Args:
            max_size_mb: Maximum allowed file size, in megabytes.
        """
        self.max_size_bytes = max_size_mb * 1024 * 1024

    def validate(self, path: Path | str) -> None:
        """Validates a PDF file.

        Args:
            path: Path to the file, as a Path or a string.

        Raises:
            FileNotFoundError: If the file does not exist.
            ValueError: If the file is not a .pdf or exceeds the size limit.
        """
        # Accept both str and Path, but work with Path from here on
        path = Path(path)

        if not path.is_file():
            raise FileNotFoundError(f"File not found: {path}")

        # Extension check only; it does not inspect the file content
        if path.suffix.lower() != ".pdf":
            raise ValueError(f"File is not a PDF: {path}")

        if path.stat().st_size > self.max_size_bytes:
            raise ValueError(f"File exceeds the size limit: {path}")