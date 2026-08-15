from dataclasses import dataclass

import attrs
from typing import final

from sqlalchemy import select, or_, func, case
from sqlalchemy.orm import sessionmaker, selectinload

from bot.infra.models import Participant

PARTICIPANTS_LIMIT = 30


class ParticipantNotFoundException(Exception):
    def __init__(self, participant_id: int):
        super().__init__(f"Participant with id {participant_id} not found")


@dataclass
class GlobalReportDTO:
    total: int
    camp: dict[int | None, int]
    infirmary: dict[int | None, int]
    left: dict[int | None, int]


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
            .limit(PARTICIPANTS_LIMIT)
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

    def global_report(self) -> GlobalReportDTO:
        with self._session_factory() as session:
            total = session.query(func.count(Participant.id)).scalar()

            stats = (
                session.query(
                    Participant.district,
                    func.sum(
                        case(
                            (Participant.status == "camp", 1), else_=0))
                            .label('camp_count'),
                    func.sum(
                        case(
                            (Participant.status == "infirmary", 1), else_=0))
                            .label('infirmary_count'),
                    func.sum(
                        case(
                            (Participant.status == "left", 1), else_=0))
                            .label('left_count')
                )
                .group_by(Participant.district)
                .all()
            )

            camp_dict = {}
            infirmary_dict = {}
            left_dict = {}

            for district, camp_count, infirmary_count, left_count in stats:
                camp_dict[district] = camp_count
                infirmary_dict[district] = infirmary_count
                left_dict[district] = left_count

        return GlobalReportDTO(
            total=total,
            camp=camp_dict,
            infirmary=infirmary_dict,
            left=left_dict
        )

    def infirmary_participants(self) -> list[Participant]:
        stmt = (
            select(Participant)
            .where(Participant.status == "infirmary")
            .order_by(Participant.full_name)
        )
        with self._session_factory() as session:
            return list(session.execute(stmt).scalars().all())

    def left_participants(self) -> list[Participant]:
        stmt = (
            select(Participant)
            .where(Participant.status == "left")
            .order_by(Participant.full_name)
        )
        with self._session_factory() as session:
            return list(session.execute(stmt).scalars().all())

    def uspen_participants(self) -> list[Participant]:
        stmt = (
            select(Participant)
            .where(Participant.star)
            .order_by(Participant.full_name)
        )
        with self._session_factory() as session:
            return list(session.execute(stmt).scalars().all())
