import attrs
from typing import final

from bot.infra.mappers import GlobalReportMapper
from bot.infra.repository import ParticipantRepo
from bot.logic.value_objects import GlobalReport


@final
@attrs.define(slots=True, frozen=True)
class GetGlobalReport:
    _repository: ParticipantRepo
    _mapper: GlobalReportMapper

    def __call__(self) -> GlobalReport:
        return self._mapper(self._repository.global_report())
