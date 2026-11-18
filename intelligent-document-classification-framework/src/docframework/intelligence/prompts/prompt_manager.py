from pathlib import Path


class PromptManager:
    def __init__(self, templates_dir: str | Path | None = None):
        if templates_dir is None:
            self.templates_dir = Path(__file__).resolve().parent / "templates"
        else:
            self.templates_dir = Path(templates_dir).resolve()

    def load_template(self, template_name: str) -> str:
        template_path = (self.templates_dir / template_name).resolve()

        if not template_path.is_relative_to(self.templates_dir.resolve()):
            raise ValueError("Template path must be inside templates directory.")

        if not template_path.is_file():
            raise FileNotFoundError(
                f"Template not found: {template_name}"
            )

        content = template_path.read_text(encoding="utf-8")

        if not content.strip():
            raise ValueError(f"Template is empty: {template_name}")

        return content
