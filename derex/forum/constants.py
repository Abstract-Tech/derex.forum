from enum import Enum


class ForumVersions(Enum):
    # Values will be passed as uppercased named arguments to the docker build
    # e.g. --build-arg FORUM_RELEASE=koa
    juniper = {
        "forum_repository": "https://github.com/edx/cs_comments_service.git",
        "forum_version": "open-release/juniper.master",
        "forum_release": "juniper",
        "docker_image_prefix": "ghcr.io/abstract-tech/derex-forum-juniper",
        "ruby_version": "2.5.7",
    }
    koa = {
        "forum_repository": "https://github.com/edx/cs_comments_service.git",
        "forum_version": "open-release/koa.master",
        "forum_release": "koa",
        "docker_image_prefix": "ghcr.io/abstract-tech/derex-forum-koa",
        "ruby_version": "2.5.7",
    }
    lilac = {
        "forum_repository": "https://github.com/edx/cs_comments_service.git",
        "forum_version": "open-release/lilac.master",
        "forum_release": "lilac",
        "docker_image_prefix": "ghcr.io/abstract-tech/derex-forum-lilac",
        "ruby_version": "2.5.7",
    }
