from typing import List

from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    ForeignKey,
    DateTime,
    Table,
    Boolean,
)
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped
from passlib.context import CryptContext


class Base(DeclarativeBase):
    pass


def create_tables(engine):
    Base.metadata.create_all(engine)


participants_subordination = Table(
    "participants_subordination",
    Base.metadata,
    Column("supervisor_id", ForeignKey("participants.id"), primary_key=True),
    Column("subordinator_id", ForeignKey("participants.id"), primary_key=True),
)


class Participant(Base):
    __tablename__ = "participants"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    full_name = Column(String, nullable=False, index=True)
    group = Column(String, nullable=True)
    birth_date = Column(Date, nullable=True)
    phone = Column(String, nullable=False)
    telegram = Column(String, nullable=False)
    vk = Column(String, nullable=True)
    status = Column(String, nullable=False)
    role = Column(String, nullable=False)
    team = Column(Integer, nullable=True)
    district = Column(Integer, nullable=True)
    health_conditions = Column(String, nullable=True)
    dietary_restrictions = Column(String, nullable=True)
    left_at = Column(DateTime, nullable=True)
    star = Column(Boolean, nullable=False, default=False)

    supervisors: Mapped[List["Participant"]] = relationship(
        secondary=participants_subordination,
        primaryjoin="Participant.id == participants_subordination.c.subordinator_id",
        secondaryjoin="Participant.id == participants_subordination.c.supervisor_id",
        back_populates="subordinates",
    )

    subordinates: Mapped[List["Participant"]] = relationship(
        secondary=participants_subordination,
        primaryjoin="Participant.id == participants_subordination.c.supervisor_id",
        secondaryjoin="Participant.id == participants_subordination.c.subordinator_id",
        back_populates="supervisors",
    )

    def __repr__(self):
        return f"<User {self.id}>"


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String, nullable=False, unique=True)
    password_hash = Column(String(255), nullable=False)

    def verify_password(self, password: str) -> bool:
        r = pwd_context.verify(password, self.password_hash)
        return r

    def __repr__(self):
        return f"<User {self.username}>"
