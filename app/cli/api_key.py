import secrets
import typer
from rich import print
from datetime import datetime, timezone, timedelta
from app.cli.utils import with_app
from app.core.application import Application
from app.models.neo4j_models import APIKey
from app.api.deps import hash_api_key

cli = typer.Typer()


@cli.command()
@with_app()
async def create(app: Application, org_name: str, name: str, days_valid: int = 30):
    org = await app.org_repo.get_by_name(org_name)
    if not org:
        print(f"[red]Error:[/red] Organization '[bold]{org_name}[/bold]' not found.")
        raise typer.Exit(code=1)

    raw_key = "cc_live_" + secrets.token_hex(32)
    expires = datetime.now(timezone.utc) + timedelta(days=days_valid)
    key_data = APIKey(
        org_id=org.id,
        name=name,
        hashed_key=hash_api_key(raw_key),
        expires_at=expires.isoformat(),
    )

    await app.api_key_repo.create(key_data)

    print("\n[green]✔ API Key created successfully[/green]")
    print(f"Organization: [cyan]{org.name}[/cyan]")
    print(f"Name:         {name}")
    print(f"Key:          [bold yellow]{raw_key}[/bold yellow]")
    print(f"Expires at:   {expires.strftime('%Y-%m-%d %H:%M:%S')} UTC")
    print("\n[dim]Note: Store this key safely. It will not be shown again.[/dim]")


@cli.command()
@with_app()
async def revoke(app: Application, key_id: str):
    await app.api_key_repo.revoke(key_id)
    print("[yellow]Key revoked[/yellow]")


@cli.command()
@with_app()
async def list(app: Application, org_id: str):
    keys = await app.api_key_repo.list(org_id)
    for r in keys:
        print(f"{r.id} | {r.name} | Active: {r.is_active}")
