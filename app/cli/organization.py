import typer
from rich import print
from app.cli.utils import with_app
from app.core.application import Application
from app.models.graph import Organization

cli = typer.Typer()


@cli.command()
@with_app()
async def create(app: Application, name: str, description: str = ""):
    org = Organization(name=name, description=description)
    await app.repo.organization.create_org(org)
    print(f"[green]Organization created[/green] ID: {org.id}")


@cli.command()
@with_app()
async def list(app: Application):
    orgs = await app.repo.organization.list_organizations()
    for r in orgs:
        print(f"{r.id} | {r.name}")


@cli.command()
@with_app()
async def delete(app: Application, org_id: str):
    await app.repo.organization.delete_org(org_id)
    print("[red]Organization deleted[/red]")
