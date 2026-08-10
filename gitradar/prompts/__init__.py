from pathlib import Path
from jinja2 import Environment, FileSystemLoader

PROMPTS_DIR = Path(__file__).parent

env = Environment(
    loader=FileSystemLoader(PROMPTS_DIR),
    trim_blocks=True,
    lstrip_blocks=True,
)


def render_prompt(template_name: str, **kwargs) -> str:
    """Render a Jinja2 prompt template with the provided context variables."""
    if not template_name.endswith(".j2"):
        template_name += ".j2"
    template = env.get_template(template_name)
    return template.render(**kwargs)
