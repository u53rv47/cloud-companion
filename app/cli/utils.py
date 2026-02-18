import asyncio
import functools
from app.core.application import Application
from app.core.migrate import get_latest_migration_version


def with_app(require_migration: bool = True):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            async def runner():
                app = Application()
                await app.start()

                try:
                    if require_migration:
                        version = await get_latest_migration_version(app.neo4j)
                        if not version:
                            raise RuntimeError("Database not migrated. Run `cc migrate` first.")
                    return await func(app, *args, **kwargs)
                finally:
                    await app.stop()

            return asyncio.run(runner())

        return wrapper

    return decorator
