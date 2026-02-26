from typing import List
from datetime import datetime
from app.schemas import omni_event_data as omni

def map_event(event: dict)-> omni.OmniEvent:
    event_id = event.get('id')
    if event_id is None:
        raise ValueError(f'Event is missing required "id" field: {event}')
    
    start_at_raw = event.get('startAt')
    start_at = datetime.fromisoformat(start_at_raw) if start_at_raw else None

    swiss_rounds = int(event['swissRounds']) if event.get('swissRounds') is not None else None

    return omni.OmniEvent(
        event_id=event_id,
        ranked=bool(event.get('ranked')),
        players=event.get('players') or [],
        judges=event.get('judges') or [],
        swiss_match_config=event.get('swissMatchConfig'),
        swiss_rounds=swiss_rounds,
        start_at=start_at,
        url=event.get('url'),
    )


def map_players(players: List[dict])-> List[omni.OmniPlayer]:
    mapped_players: List[omni.OmniPlayer] = []

    for player in players:
        username = (player.get('username') or '')
        username = username.title()

        player_cp = int(player.get('cp') or 0)

        mapped_players.append(
            omni.OmniPlayer(
                player_id= player.get('id'),
                username= username,
                country= player.get('country'),
                player_cp= player_cp,
                player_rank= player.get('rank'),
                player_emblem= player.get('emblem'),
            )
        )

    return mapped_players

def map_standings(event_id: int, standings: dict)-> List[omni.OmniEventStanding]:
    mapped_standings: List[omni.OmniEventStanding] = []

    players: List[dict] = standings.get('standings') or []

    for placement, standing in enumerate(players, start=1):
        mapped_standings.append(
            omni.OmniEventStanding(
                event_id=event_id,
                player_id=standing.get('id'),
                placement=placement,
                wins=standing.get('statsWins'),
                losses=standing.get('statsLosses'),
                ties=standing.get('statsTies'),
                byes=standing.get('statsByes'),
                score=standing.get('statsScore'),
            )
        )
    
    return mapped_standings

def map_participants(event_id: int, rounds: List[dict])-> List[omni.OmniEventParticipant]:
    mapped_participants: List[omni.OmniEventParticipant] = []

    for r in rounds:
        round_id = r['round']['id']
        pairings: List[dict] = r.get('pairings', [])

        for pairing in pairings:
            pairing_id = pairing.get('id')
            participants: List[dict] = pairing.get('pairing', [])

            for participant in participants:
                mapped_participants.append(
                    omni.OmniEventParticipant(
                        event_id=event_id,
                        player_id=participant.get('id'),
                        round_id=round_id,
                        pairing_id=pairing_id,
                        dropped=participant.get('dropped', False),
                        score=participant.get('score', 0),
                        status=participant.get('status'),
                        elo_change=participant.get('eloChange', 0.0)
                    )
                )
    
    return mapped_participants