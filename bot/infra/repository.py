import attrs
from typing import final, cast

from sqlalchemy import select, or_, and_
from sqlalchemy.orm import sessionmaker, selectinload

from bot.infra.models import Participant


class ParticipantNotFoundException(Exception):
    def __init__(self, participant_id: int):
        super().__init__(f"Participant with id {participant_id} not found")


@final
@attrs.define(slots=True, frozen=True)
class ParticipantRepo:
    _session_factory: sessionmaker

    def search_participants(self, query: str) -> list[Participant]:
        stmt = (
            select(Participant)
            .where(
                or_(
                    Participant.full_name.ilike(f"%{query}%"),
                    Participant.telegram.ilike(f"%{query}%"),
                )
            )
            .order_by(Participant.full_name)
        )
        with self._session_factory() as session:
            return list(session.execute(stmt).scalars().all())

    def get_participant(self, participant_id: int) -> Participant:
        stmt = (
            select(Participant)
            .where(Participant.id == participant_id)
            .options(
                selectinload(Participant.supervisors),
                selectinload(Participant.subordinates),
            )
        )
        with self._session_factory() as session:
            participant = session.execute(stmt).scalars().one_or_none()
            if participant is None:
                raise ParticipantNotFoundException(participant_id)
            return participant

    def team_participants(self, team: int) -> list[Participant]:
        stmt = (
            select(Participant)
            .where(Participant.team == team)
            .order_by(Participant.full_name)
        )
        with self._session_factory() as session:
            return list(session.execute(stmt).scalars().all())
