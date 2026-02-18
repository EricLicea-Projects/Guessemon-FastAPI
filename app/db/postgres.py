import asyncpg

async def init_pg_pool(app, dsn: str) -> None:
    app.state.pg_pool = await asyncpg.create_pool(
        dsn=dsn,
        min_size=1,
        max_size=10,
    )


async def close_pg_pool(app) -> None:
    pool = getattr(app.state, 'pg_pool', None)
    if pool:
        await pool.close()
