import attrs
from typing import final

from bot.infra.mappers import ParticipantDetailedMapper
from bot.infra.repository import ParticipantRepo
from bot.logic.value_objects import ParticipantDetailed


@final
@attrs.define(slots=True, frozen=True)
class GetParticipant:
    _repository: ParticipantRepo
    _mapper: ParticipantDetailedMapper

    def __call__(self, participant_id: int) -> ParticipantDetailed:
        return self._mapper(self._repository.get_participant(participant_id))
