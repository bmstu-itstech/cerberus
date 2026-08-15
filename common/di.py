from typing import Any, final

import punq

from bot.infra.models import create_tables
from common.config import Config


class HasContainer:
    __slots__ = ("_container",)

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._container = populate_dependencies(punq.Container())

    @final
    def resolve[Thing](self, thing: type[Thing]) -> Thing:
        return self._container.resolve(thing)


def _populate_sqlalchemy(container: punq.Container) -> punq.Container:
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker

    config = container.resolve(Config)

    engine = create_engine(str(config.pg_dsn))
    session_factory = sessionmaker(
        bind=engine,
        autocommit=False,
        autoflush=False,
    )
    create_tables(engine)

    container.register(engine, instance=engine)
    container.register(sessionmaker, instance=session_factory)
    return container


def _populate_app(container: punq.Container) -> punq.Container:
    from bot.infra import mappers, repository
    from bot.logic import usecases

    container.register(repository.ParticipantRepo)

    container.register(mappers.ParticipantLinkMapper)
    container.register(mappers.ParticipantDetailedMapper)

    container.register(usecases.SearchParticipants)
    container.register(usecases.GetParticipant)
    container.register(usecases.GetTeam)

    return container


def populate_dependencies(container: punq.Container) -> punq.Container:
    config = Config.from_env()
    container.register(Config, instance=config)
    _populate_sqlalchemy(container)
    _populate_app(container)
    return container
