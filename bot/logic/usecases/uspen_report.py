import attrs
from typing import final

from bot.infra.mappers import ParticipantLinkMapper
from bot.infra.repository import ParticipantRepo
from bot.logic.value_objects import UspenReport


@final
@attrs.define(slots=True, frozen=True)
class GetUspenReport:
    _repository: ParticipantRepo
    _mapper: ParticipantLinkMapper

    def __call__(self) -> UspenReport:
        return UspenReport(
            participants=[
                self._mapper(p) for p in self._repository.uspen_participants()
            ]
        )
