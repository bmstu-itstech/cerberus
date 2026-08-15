from jinja2 import Environment, FileSystemLoader


env = Environment(
    loader=FileSystemLoader("templates"),
)


def render(template_name: str, **kwargs) -> str:
    template = env.get_template(template_name)
    return template.render(**kwargs)
