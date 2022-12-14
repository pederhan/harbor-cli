from __future__ import annotations

from typing import Optional

import typer
from harborapi.models.models import Repository

from ...logs import logger
from ...output.render import render_result
from ...state import state
from ...utils.utils import inject_help
from ...utils.utils import inject_resource_options


# Create a command group
app = typer.Typer(
    name="repository",
    help="Manage repositories.",
    no_args_is_help=True,
)


# HarborAsyncClient.get_repository()
@app.command("get", no_args_is_help=True)
def get_repo(
    ctx: typer.Context,
    project: str = typer.Argument(
        ...,
        help="Name of the project the repository belongs to.",
    ),
    repository: str = typer.Argument(
        ...,
        help="Name of the repository to get.",
    ),
) -> None:
    """Fetch a repository."""

    # TODO: accept single arg like in `harbor-cli artifact get`?

    repo = state.run(
        state.client.get_repository(
            project,
            repository,
        ),
        "Fetching repository...",
    )
    render_result(repo, ctx)


# HarborAsyncClient.delete_repository()
@app.command("delete", no_args_is_help=True)
def delete_artifact(
    ctx: typer.Context,
    project: str = typer.Argument(
        ...,
        help="Name of the project the repository belongs to.",
    ),
    repository: str = typer.Argument(
        ...,
        help="Name of the repository to get.",
    ),
    force: bool = typer.Option(
        False,
        "--force",
        "-f",
        help="Skip confirmation prompt.",
    ),
) -> None:
    """Delete a repository."""
    if not force:
        typer.confirm(
            f"Are you sure you want to delete {project}/{repository}?",
            abort=True,
        )
    state.run(
        state.client.delete_repository(
            project,
            repository,
        ),
        "Deleting repository...",
    )
    logger.info(f"Deleted {project}/{repository}.")


# HarborAsyncClient.update_repository()
@app.command("update")
@inject_help(Repository)
def update_repository(
    ctx: typer.Context,
    project: str = typer.Argument(
        ...,
        help="Name of the project the repository belongs to.",
    ),
    repository: str = typer.Argument(
        ...,
        help="Name of the repository to get.",
    ),
    description: Optional[str] = typer.Option(None),
) -> None:
    """Update a repository.

    As of now, only the description can be updated (if the Web UI is to be trusted).
    """
    state.run(
        state.client.update_repository(
            project,
            repository,
            Repository(description=description),
        )
    )
    logger.info(f"Updated {project}/{repository}.")


# HarborAsyncClient.get_repositories()
@app.command("list")
@inject_resource_options()
def list_repos(
    ctx: typer.Context,
    project: Optional[str] = typer.Argument(
        None,
        help="Name of project to fetch repositories from. If not specified, all projects will be searched.",
    ),
    query: Optional[str] = None,
    sort: Optional[str] = None,
    page: int = 1,
    page_size: int = 10,
    retrieve_all: bool = True,
) -> None:
    """List repositories in all projects or a specific project."""

    repos = state.run(
        state.client.get_repositories(
            project,
            query=query,
            sort=sort,
            page=page,
            page_size=page_size,
            retrieve_all=retrieve_all,
        ),
        "Fetching repositories...",
    )
    render_result(repos, ctx)
