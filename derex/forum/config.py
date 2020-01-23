import logging
import pkg_resources
from typing import List, Dict, Union

from derex import runner  # type: ignore


class ForumService:
    @staticmethod
    @runner.hookimpl
    def local_compose_options() -> Dict[str, Union[str, List[str]]]:
        options = [
            "-f",
            pkg_resources.resource_filename(__name__, "docker-compose.yml")
        ]
        return {
            "options": options,
            "name": "forum",
            "priority": ">base",
            "variant": "openedx",
        }
