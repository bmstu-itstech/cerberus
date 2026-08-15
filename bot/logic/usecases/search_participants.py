import attrs
from typing import final

from bot.infra.mappers import ParticipantLinkMapper
from bot.infra.repository import ParticipantRepo
from bot.logic.value_objects import ParticipantLink


@final
@attrs.define(slots=True, frozen=True)
class SearchParticipants:
    _repository: ParticipantRepo
    _mapper: ParticipantLinkMapper

    def __call__(self, query: str) -> list[ParticipantLink]:
        return [self._mapper(p) for p in self._repository.search_participants(query)]
