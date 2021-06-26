import urllib.parse
from pathlib import Path
from typing import Dict, List, Union

import pkg_resources
from derex.runner.constants import MONGODB_ROOT_USER
from derex.runner.mongodb import MONGODB_ROOT_PASSWORD
from derex.runner.project import Project
from jinja2 import Template

from derex import runner  # type: ignore
from derex.forum import __version__
from derex.forum.constants import ForumVersions


def generate_local_docker_compose(project: Project) -> Path:
    derex_dir = project.root / ".derex"
    if not derex_dir.is_dir():
        derex_dir.mkdir()
    local_compose_path = derex_dir / "docker-compose-forum.yml"
    template_path = Path(
        pkg_resources.resource_filename(__name__, "docker-compose-forum.yml.j2")
    )
    default_docker_image_prefix = ForumVersions[project.openedx_version.name].value[
        "docker_image_prefix"
    ]
    forum_docker_image = project.config.get(
        "forum_docker_image", f"{default_docker_image_prefix}:{__version__}"
    )
    mongodb_root_user = urllib.parse.quote_plus(MONGODB_ROOT_USER)
    mongodb_root_password = urllib.parse.quote_plus(MONGODB_ROOT_PASSWORD)
    tmpl = Template(template_path.read_text())
    text = tmpl.render(
        project=project,
        forum_docker_image=forum_docker_image,
        MONGODB_ROOT_USER=mongodb_root_user,
        MONGODB_ROOT_PASSWORD=mongodb_root_password,
    )
    local_compose_path.write_text(text)
    return local_compose_path


class ForumService:
    @staticmethod
    @runner.hookimpl
    def ddc_project_options(project: Project) -> Dict[str, Union[str, List[str]]]:
        options: List[str] = []
        if "derex.forum" in project.config.get("plugins", {}):
            local_compose_path = generate_local_docker_compose(project)
            options = ["-f", str(local_compose_path)]
        return {
            "options": options,
            "name": "forum",
            "priority": "<local-project",
        }
