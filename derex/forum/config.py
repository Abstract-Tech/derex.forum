from pathlib import Path
from typing import Dict, List, Union

import pkg_resources

from derex import runner  # type: ignore
from derex.runner.project import Project
from jinja2 import Template


def generate_local_docker_compose(project: Project) -> Path:
    derex_dir = project.root / ".derex"
    if not derex_dir.is_dir():
        derex_dir.mkdir()
    local_compose_path = derex_dir / "docker-compose-forum.yml"
    template_path = Path(
        pkg_resources.resource_filename(__name__, "docker-compose-forum.yml.j2")
    )
    forum_docker_image = project.config.get(
        "forum_docker_image", "derex/forum:ironwood"
    )
    tmpl = Template(template_path.read_text())
    text = tmpl.render(project=project, forum_docker_image=forum_docker_image)
    local_compose_path.write_text(text)
    return local_compose_path


class ForumService:
    @staticmethod
    @runner.hookimpl
    def local_compose_options(project: Project) -> Dict[str, Union[str, List[str]]]:
        if "derex.forum" in project.config.get("plugins", {}):
            local_compose_path = generate_local_docker_compose(project)
            options = ["-f", str(local_compose_path)]
            return {
                "options": options,
                "name": "forum",
                "priority": ">base",
                "variant": "openedx",
            }
        return {}
