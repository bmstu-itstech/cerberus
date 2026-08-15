from jinja2 import Environment, FileSystemLoader, select_autoescape


env = Environment(
    loader=FileSystemLoader("bot/templates"),
    autoescape=select_autoescape(["html", "xml"])
)

def render_template(template_name: str, **kwargs) -> str:
    template = env.get_template(template_name)
    return template.render(**kwargs)
