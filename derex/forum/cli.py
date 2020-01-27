import click
from derex.runner.cli import ensure_project


@click.command("provision-forum")
@click.pass_obj
@ensure_project
def provision_forum_cmd(project):
    """Prime the elasticsearch index for the forum service"""
    from derex.runner.docker import check_services
    from derex.runner.compose_utils import run_compose

    if "derex.forum" not in project.config.get("plugins", {}):
        click.echo(
            "Forum is not enabled for this project.\n"
            "Enable it by installing the derex.forum plugin."
        )
        return

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
