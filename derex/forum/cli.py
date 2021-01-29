import sys

import click
from derex.runner.cli import ensure_project


@click.group()
@click.pass_context
def forum(ctx):
    """Derex edX Forum plugin: commands to manage the Open edX Forum service
    """
    pass


@forum.command("create-index")
@click.pass_obj
@ensure_project
def create_index(project):
    """Prime the elasticsearch index for the Forum service"""
    from derex.runner.docker_utils import wait_for_service
    from derex.runner.ddc import run_ddc_project

    try:
        wait_for_service("elasticsearch")
    except (TimeoutError, RuntimeError, NotImplementedError) as exc:
        click.echo(click.style(str(exc), fg="red"))
        sys.exit(1)

    compose_args = [
        "run",
        "--rm",
        "-T",
        "forum",
        "sh",
        "-c",
        """bundle exec rake search:initialize &&
        bundle exec rake search:rebuild_index
        """,
    ]
    run_ddc_project(compose_args, project=project)
    return 0
