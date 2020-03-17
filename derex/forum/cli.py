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
    from derex.runner.docker import check_services
    from derex.runner.compose_utils import run_compose

    if not check_services(["elasticsearch"]):
        click.echo(
            "Elasticsearch service not found.\nMaybe you forgot to run\nddc-services up -d"
        )
        return

    args = [
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
    run_compose(args, project=project)
    return 0
