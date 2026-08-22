import attrs
from typing import final

from bot.infra.mappers import ParticipantLinkMapper
from bot.infra.repository import ParticipantRepo
from bot.logic.value_objects import InfirmaryReport


@final
@attrs.define(slots=True, frozen=True)
class GetInfirmaryReport:
    _repository: ParticipantRepo
    _mapper: ParticipantLinkMapper

    def __call__(self) -> InfirmaryReport:
        return InfirmaryReport(
            participants=[
                self._mapper(p) for p in self._repository.infirmary_participants()
            ]
        )
