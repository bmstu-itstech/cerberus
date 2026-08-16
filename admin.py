from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse

from sqladmin import Admin, ModelView
from sqladmin.authentication import AuthenticationBackend
from sqladmin.filters import AllUniqueStringValuesFilter, BooleanFilter
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from bot.infra.models import Participant, User
from common.config import Config
from common.di import HasContainer


resolver = HasContainer()
config = resolver.resolve(Config)
engine = create_engine(str(config.pg_dsn))


class ParticipantAdmin(ModelView, model=Participant):
    page_size = 100

    column_list = [
        Participant.id,
        Participant.full_name,
        Participant.group,
        Participant.birth_date,
        Participant.phone,
        Participant.telegram,
        Participant.vk,
        Participant.status,
        Participant.role,
        Participant.team,
        Participant.district,
        Participant.health_conditions,
        Participant.dietary_restrictions,
        Participant.star,
        Participant.supervisors,
        Participant.subordinates,
    ]
    column_searchable_list = [
        Participant.id,
        Participant.full_name,
    ]
    column_filters = [
        AllUniqueStringValuesFilter(Participant.role),
        AllUniqueStringValuesFilter(Participant.status),
        BooleanFilter(Participant.star),
    ]
    column_formatters = {
        Participant.supervisors: lambda obj, _: [s.full_name for s in obj.supervisors],
        Participant.subordinates: lambda obj, _: [s.full_name for s in obj.subordinates],
    }


class AuthBackend(AuthenticationBackend):
    def __init__(self, secret_key: str, session_maker):
        super().__init__(secret_key)
        self.session_maker = session_maker

    async def login(self, request: Request) -> bool | RedirectResponse:
        try:
            form = await request.form()
            username = form.get("username")
            password = form.get("password")

            if not username or not password:
                return False

            with self.session_maker() as db_session:
                user = db_session.query(User).filter(User.username == username).first()

                if user and user.verify_password(password):
                    request.session.update({
                        "user_id": user.id,
                        "username": user.username,
                    })
                    return True

            return False

        except Exception as e:
            print(f"Ошибка при входе: {e}")
            return False

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        user_id = request.session.get("user_id")
        if not user_id:
            return False

        with self.session_maker() as db_session:
            user = db_session.query(User).filter(User.id == user_id).first()
            return user is not None


app = FastAPI()
session_factory = resolver.resolve(sessionmaker)
admin = Admin(app, engine, authentication_backend=AuthBackend(config.secret, session_factory))
admin.add_view(ParticipantAdmin)
