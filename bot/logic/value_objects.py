from enum import StrEnum
from dataclasses import dataclass
from datetime import date, datetime


class Role(StrEnum):
    PARTICIPANT = "participant"
    TS_TEAM = "ts_team"
    MEDIA_TEAM = "media_team"
    HQ_TEAM = "hq_team"
    EP_TEAM = "ep_team"
    SENIOR_TEAM = "senior_team"
    CURATOR = "curator"
    PRESENTER = "presenter"
    HEAD_OF_TEAM = "head_of_team"
    STAGE_TEAM = "sc_team"
    SECURITY_TEAM = "security_team"
    MEDICINE_TEAM = "medicine_team"
    SENIOR_CURATOR = "senior_curator"

    @property
    def display_name(self) -> str:
        return {
            self.PARTICIPANT: "участник",
            self.TS_TEAM: "техническая поддержка",
            self.MEDIA_TEAM: "медиа",
            self.HQ_TEAM: "штаб",
            self.EP_TEAM: "образовательные площадки",
            self.SENIOR_TEAM: "старший оргкомитет",
            self.CURATOR: "куратор",
            self.PRESENTER: "ведущий",
            self.HEAD_OF_TEAM: "руководитель проекта",
            self.STAGE_TEAM: "команда сцены",
            self.SECURITY_TEAM: "служба безопасности",
            self.MEDICINE_TEAM: "медицина",
            self.SENIOR_CURATOR: "старшие кураторы",
        }[self]

    @property
    def emoji(self) -> str:
        return {
            self.PARTICIPANT: "",
            self.TS_TEAM: "⚫",
            self.MEDIA_TEAM: "🟢",
            self.HQ_TEAM: "🟡",
            self.EP_TEAM: "🔵",
            self.SENIOR_TEAM: "⚪️",
            self.CURATOR: "🔴",
            self.PRESENTER: "💜",
            self.HEAD_OF_TEAM: "🤍",
            self.STAGE_TEAM: "🟣",
            self.SECURITY_TEAM: "🟤",
            self.MEDICINE_TEAM: "🩵",
            self.SENIOR_CURATOR: "🟠",
        }[self]


class Status(StrEnum):
    CAMP = "camp"
    INFIRMARY = "infirmary"
    LEFT = "left"

    @property
    def display_name(self) -> str:
        return {
            self.CAMP: "в лагере",
            self.INFIRMARY: "в лазарете",
            self.LEFT: "покинул лагерь",
        }[self]

    @property
    def emoji(self) -> str:
        return {
            self.CAMP: "🏕️",
            self.INFIRMARY: "🏥",
            self.LEFT: "💼",
        }[self]


@dataclass
class ParticipantLink:
    id: int
    full_name: str
    role: Role
    status: Status
    team: int | None
    district: int | None
    star: bool

    @property
    def display_name(self) -> str:
        s = self.full_name
        if self.star:
            s += " 😎"
        return s


@dataclass
class ParticipantDetailed:
    id: int
    full_name: str
    group: str | None
    birth_date: date | None
    phone: str
    telegram: str
    vk: str | None
    status: Status
    left_at: datetime | None
    role: Role
    team: int | None
    district: int | None
    health_conditions: str | None
    dietary_restrictions: str | None
    star: bool
    contacts: str | None
    partners: list[ParticipantLink]
    supervisors: list[ParticipantLink]
    subordinates: list[ParticipantLink]

    @property
    def display_name(self) -> str:
        s = self.full_name
        if self.star:
            s += "😎"
        return s

    @property
    def age(self) -> int | None:
        if self.birth_date is None:
            return None
        today = date.today()
        # Расчёт возраста производится грубой оценкой по
        # разности текущего года и года рождения, после чего
        # осуществляется поправка с учётом конкретных дат
        return (
            today.year
            - self.birth_date.year
            - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))
        )


@dataclass
class TeamInfo:
    team: int
    district: int
    curators: list[ParticipantLink]
    participants: list[ParticipantLink]


@dataclass
class GlobalReport:
    total: int
    # Словарь округ -> количество человек в округе с данным статусом
    # None соответствует организаторам без округа
    camp: dict[int | None, int]
    infirmary: dict[int | None, int]
    left: dict[int | None, int]


@dataclass
class InfirmaryReport:
    participants: list[ParticipantLink]


@dataclass
class LeftReport:
    participants: list[ParticipantLink]


@dataclass
class UspenReport:
    participants: list[ParticipantLink]
