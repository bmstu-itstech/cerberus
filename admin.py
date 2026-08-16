from fastapi import FastAPI
from sqladmin import Admin, ModelView
from sqladmin.filters import AllUniqueStringValuesFilter, BooleanFilter
from sqlalchemy import create_engine

from bot.infra.models import Participant
from common.config import Config
from common.di import HasContainer


resolver = HasContainer()
config = resolver.resolve(Config)
engine = create_engine(str(config.pg_dsn))
app = FastAPI()
admin = Admin(app, engine)


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


admin.add_view(ParticipantAdmin)