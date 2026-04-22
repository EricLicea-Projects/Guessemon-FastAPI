import asyncpg
from app.schemas.local_dex_data import PlayerStats

async def get_player_stats(conn: asyncpg.Connection) -> list[PlayerStats]:
    query = "SELECT * FROM player_stats_table;"
    rows = await conn.fetch(query)

    players: dict[int, PlayerStats] = {}

    for row in rows:
        pid = row["player_id"]

        if pid not in players:
            players[pid] = PlayerStats(
                player_id=pid,
                username=row["username"],
                player_cp=row["player_cp"],
                total_wins=row['total_wins'],
                total_losses=row['total_losses'],
                total_games=row['total_games'],
                win_rate=float(row["win_rate"]),
                main_element=row["main_element"],
                top_3_champions=[]
            )

        players[pid].top_3_champions.append(row["champion_name"])

    return list(players.values())