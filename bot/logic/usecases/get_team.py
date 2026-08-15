import attrs
from typing import final

from bot.infra.mappers import ParticipantLinkMapper
from bot.infra.repository import ParticipantRepo
from bot.logic.value_objects import TeamInfo, Role, Status


@final
@attrs.define(slots=True, frozen=True)
class GetTeam:
    _repository: ParticipantRepo
    _mapper: ParticipantLinkMapper

    def __call__(self, team: int) -> TeamInfo:
        heap = [self._mapper(p) for p in self._repository.team_participants(team)]
        if not heap:
            return TeamInfo(team=team, district=0, curators=[], participants=[])
        district = heap[0].district or 0
        prts = [
            p for p in heap if p.role == Role.PARTICIPANT and p.status != Status.LEFT
        ]
        curators = [p for p in heap if p.role == Role.CURATOR]
        return TeamInfo(
            team=team,
            district=district,
            curators=curators,
            participants=prts,
        )
