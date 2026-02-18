import typer
from app.cli.utils import with_app
from app.core.migrate import run_migrations

cli = typer.Typer()


@cli.command()
@with_app(require_migration=False)
async def migrate(app):
    await run_migrations(app.neo4j)
    print("Migrations applied successfully.")
