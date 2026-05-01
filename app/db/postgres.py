import asyncpg


async def create_pg_pool(dsn: str) -> asyncpg.Pool:
    return await asyncpg.create_pool(
        dsn=dsn,
        min_size=1,
        max_size=10,
    )


async def close_pg_pool(pool: asyncpg.Pool | None) -> None:
    if pool is not None:
        await pool.close()