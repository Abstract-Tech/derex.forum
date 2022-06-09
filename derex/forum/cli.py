import os
import sys
from distutils.spawn import find_executable

import click
from derex.runner.cli import ensure_project
from derex.runner.cli.build import build as derex_build_cli
from derex.runner.utils import abspath_from_egg

from derex.forum import __version__
from derex.forum.constants import ForumVersions


@click.group()
@click.pass_context
def forum(ctx):
    """Derex edX Forum plugin: commands to manage the Open edX Forum service"""
    pass


@forum.command("create-index")
@click.pass_obj
@ensure_project
def create_index(project):
    """Prime the elasticsearch index for the Forum service"""
    from derex.runner.ddc import run_ddc_project
    from derex.runner.docker_utils import wait_for_service

    try:
        if project.openedx_version.name == "lilac":
            wait_for_service("elasticsearch7")
        else:
            wait_for_service("elasticsearch")
    except (TimeoutError, RuntimeError, NotImplementedError) as exc:
        click.echo(click.style(str(exc), fg="red"))
        sys.exit(1)

    if project.openedx_version.name == "lilac":
        cmd = "bundle exec rake search:initialize && bundle exec rake search:rebuild_indices"
    else:
        cmd = "bundle exec rake search:initialize && bundle exec rake search:rebuild_index"

    compose_args = [
        "run",
        "--rm",
        "-T",
        "forum",
        "sh",
        "-c",
        cmd,
    ]
    run_ddc_project(compose_args, project)
    return 0


@forum.command("rebuild-indices")
@click.pass_obj
@ensure_project
def rebuild_indices(project):
    """Rebuild the elasticsearch index for the Forum service"""
    from derex.runner.ddc import run_ddc_project
    from derex.runner.docker_utils import wait_for_service

    try:
        if project.openedx_version.name == "lilac":
            wait_for_service("elasticsearch7")
        else:
            wait_for_service("elasticsearch")
    except (TimeoutError, RuntimeError, NotImplementedError) as exc:
        click.echo(click.style(str(exc), fg="red"))
        sys.exit(1)

    if project.openedx_version.name == "lilac":
        cmd = "bundle exec rake search:rebuild_indices"
    else:
        cmd = "bundle exec rake search:rebuild_index"

    compose_args = [
        "run",
        "--rm",
        "-T",
        "forum",
        "sh",
        "-c",
        cmd,
    ]
    run_ddc_project(compose_args, project)
    return 0


@derex_build_cli.command("forum")
@click.argument(
    "version",
    type=click.Choice(ForumVersions.__members__),
    required=True,
    callback=lambda _, __, value: value and ForumVersions[value],
)
@click.option(
    "--push/--no-push", default=False, help="Also push image to registry after building"
)
@click.option(
    "--only-print-image-name/--do-build",
    default=False,
    help="Only print image name",
)
@click.option(
    "-d",
    "--docker-opts",
    envvar="DOCKER_OPTS",
    default="--output type=image,name={docker_image_prefix}{push_arg}",
    help=(
        "Additional options to pass to the docker invocation.\n"
        "By default outputs the image to the local docker daemon."
    ),
)
def forum_build(version, push, only_print_image_name, docker_opts):
    # TODO: generalize derex.runner build.openedx function so to
    # take the dockerfile_dir and secrets as arguments.
    # This way we can avoid repeating code here and just call
    # the build function with our arguments.
    # e.g.
    # return derex_build_cli.build(
    #     dockerfile_dir,
    #     version,
    #     push,
    #     only_print_image_name,
    #     docker_opts,
    #     secrets
    # )
    """Build openedx image using docker. Defaults to dev image target."""
    dockerfile_dir = abspath_from_egg("derex.forum", "docker_build/Dockerfile").parent
    build_arguments = []
    for spec in version.value.items():
        build_arguments.append("--build-arg")
        build_arguments.append(f"{spec[0].upper()}={spec[1]}")
    docker_image_prefix = version.value["docker_image_prefix"]
    image_name = f"{docker_image_prefix}:{__version__}"
    if only_print_image_name:
        click.echo(image_name)
        return
    push_arg = ",push=true" if push else ""
    command = [
        "docker",
        "buildx",
        "build",
        str(dockerfile_dir),
        "-t",
        image_name,
        *build_arguments,
    ]
    if docker_opts:
        command.extend(docker_opts.format(**locals()).split())
    print("Invoking\n" + " ".join(command), file=sys.stderr)
    os.execve(find_executable(command[0]), command, os.environ)
