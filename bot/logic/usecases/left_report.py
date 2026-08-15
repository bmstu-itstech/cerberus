import attrs
from typing import final

from bot.infra.mappers import ParticipantLinkMapper
from bot.infra.repository import ParticipantRepo
from bot.logic.value_objects import LeftReport


@final
@attrs.define(slots=True, frozen=True)
class GetLeftReport:
    _repository: ParticipantRepo
    _mapper: ParticipantLinkMapper

    def __call__(self) -> LeftReport:
        return LeftReport(
            participants=[self._mapper(p) for p in self._repository.left_participants()]
        )
