from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    ForeignKey,
    DateTime,
    PrimaryKeyConstraint,
)
from sqlalchemy.orm import relationship


class Participant(Base):
    __tablename__ = "participants"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    full_name = Column(String, nullable=False, index=True)
    group = Column(String, nullable=True)
    birth_date = Column(Date, nullable=True)
    phone = Column(String, nullable=False)
    telegram = Column(String, nullable=False)
    status = Column(String, nullable=False)
    role = Column(String, nullable=False)
    team = Column(Integer, nullable=True)
    district = Column(Integer, nullable=True)
    health_conditions = Column(String, nullable=True)
    dietary_restrictions = Column(String, nullable=True)
    left_at = Column(DateTime, nullable=True)

    supervisors = relationship(
        "ParticipantRelationship",
        foreign_keys="ParticipantRelationship.subordinator_id",
        back_populates="supervisor",
    )

    subordinates = relationship(
        "ParticipantRelationship",
        foreign_keys="ParticipantRelationship.supervisor_id",
        back_populates="subordinator",
    )


class ParticipantRelationship(Base):
    __tablename__ = "participants_relationships"

    supervisor_id: Column = Column(
        Integer,
        ForeignKey("participants.id"),
        nullable=False,
    )

    subordinator_id: Column = Column(
        Integer,
        ForeignKey("participants.id"),
        nullable=False,
    )

    supervisor = relationship(
        "Participant",
        foreign_keys=[supervisor_id],
        back_populates="subordinates",
    )

    subordinator = relationship(
        "Participant",
        foreign_keys=[subordinator_id],
        back_populates="supervisors",
    )

    __table_args__ = (PrimaryKeyConstraint(supervisor_id, subordinator_id),)
