import typer
from rich import print
from typing import Annotated
from app.cli.utils import with_app
from app.core.constants import CloudProvider
from app.core.application import Application
from app.models.graph import Account

cli = typer.Typer()


@cli.command()
@with_app()
async def create(
    app: Application,
    org_name: str,
    name: str,
    provider: Annotated[CloudProvider, typer.Argument(help="Cloud provider (aws, azure, gcp)")],
    account_id: str,
):
    org = await app.repo.organization.get_org_by_name(org_name)
    if not org:
        print(f"[red]Error:[/red] Organization '[bold]{org_name}[/bold]' not found.")
        raise typer.Exit(code=1)

    acc = Account(
        org_id=org.id,
        name=name,
        provider=provider,
        account_id=account_id,
    )

    await app.repo.organization.create_account(acc)
    print(f"[green]Cloud account created for [bold]{provider.value}[/bold][/green]")


@cli.command()
@with_app()
async def list(app: Application, org_id: str):
    accounts = await app.repo.organization.list_accounts(org_id)
    for r in accounts:
        print(f"{r.account_id} | {r.name} | [bold cyan]{r.provider.value}[/bold cyan]")
