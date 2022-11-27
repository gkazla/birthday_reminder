from typing import Optional

from jinja2 import FileSystemLoader, Environment


class CommunityTemplate:
    def __init__(self, template_directory: Optional[str] = None) -> None:
        self.__template_environment = Environment(
            loader=FileSystemLoader(template_directory or './')
        )

    def render(self, template_file_name: str, **kwargs) -> str:
        template = self.__template_environment.get_template(template_file_name)

        return template.render(kwargs)
