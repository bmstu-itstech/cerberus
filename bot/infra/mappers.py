from datetime import date, datetime

import attrs
from typing import final, cast

from bot.logic.value_objects import (
    ParticipantDetailed,
    ParticipantLink,
    Status,
    Role, GlobalReport,
)

from .models import Participant
from .repository import GlobalReportDTO


@final
@attrs.define(slots=True, frozen=True)
class ParticipantLinkMapper:
    def __call__(self, participant: Participant) -> ParticipantLink:
        return ParticipantLink(
            id=int(participant.id),
            full_name=str(participant.full_name),
            role=Role(str(participant.role)),
            status=Status(str(participant.status)),
            team=cast(int | None, participant.team),
            district=cast(int | None, participant.district),
            star=bool(participant.star),
        )


@final
@attrs.define(slots=True, frozen=True)
class ParticipantDetailedMapper:
    def __call__(self, participant: Participant) -> ParticipantDetailed:
        link_mapper = ParticipantLinkMapper()
        return ParticipantDetailed(
            id=int(participant.id),
            full_name=str(participant.full_name),
            group=str(participant.group),
            birth_date=cast(date | None, participant.birth_date),
            phone=str(participant.phone),
            telegram=str(participant.telegram),
            vk=cast(str | None, participant.vk),
            status=Status(str(participant.status)),
            left_at=cast(datetime | None, participant.left_at),
            role=Role(str(participant.role)),
            team=cast(int | None, participant.team),
            district=cast(int | None, participant.district),
            health_conditions=cast(str | None, participant.health_conditions),
            dietary_restrictions=cast(str | None, participant.dietary_restrictions),
            star=bool(participant.star),
            supervisors=[link_mapper(p) for p in participant.supervisors],
            subordinates=[link_mapper(p) for p in participant.subordinates],
        )

@final
@attrs.define(slots=True, frozen=True)
class GlobalReportMapper:
    def __call__(self, report: GlobalReportDTO) -> GlobalReport:
        return GlobalReport(
            total=report.total,
            camp=report.camp,
            infirmary=report.infirmary,
            left=report.left,
        )
