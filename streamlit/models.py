from sqlalchemy import Column, ForeignKey, String, Double, Integer, Boolean, DateTime, Time, DDL, UniqueConstraint, event
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import relationship
# from sqlalchemy.schema import UniqueConstraint


class Base(DeclarativeBase):
    pass


class OU(Base):
    __tablename__ = "organization_unit"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nexus_name = Column(String(30), nullable=False)
    nexus_id = Column(Integer, nullable=True)
    vitacomm_name = Column(String(30))
    applikator_id = Column(Integer)

    parent_id = Column(Integer, ForeignKey("organization_unit.id"), nullable=True)
    parent = relationship("OU", remote_side=[id], back_populates="children", lazy='subquery')
    children = relationship("OU", back_populates="parent")

    weekly_stats = relationship("WeeklyStat", back_populates="ou", cascade="all, delete-orphan")
    services = relationship("Service", back_populates="ou", cascade="all, delete-orphan")

    __table_args__ = (UniqueConstraint('nexus_name', 'vitacomm_name', name='unique_ou'),)
    # __table_args__ = (
    #     UniqueConstraint('nexus_name', 'vitacomm_name', name='unique_ou'),
    #     DDL('CREATE UNIQUE INDEX unique_nexus_vitacomm ON organization_unit (nexus_name) WHERE vitacomm_name IS NULL')
    # )

    def __repr__(self) -> str:
        return f"OU(id={self.id!r}, nexus={self.nexus_name!r}, vitacomm={self.vitacomm_name!r}, applikator={self.applikator_id!r})"


@event.listens_for(OU.__table__, 'after_create')
def create_partial_index(target, connection, **kwargs):
    connection.execute(DDL('CREATE UNIQUE INDEX unique_nexus ON organization_unit (nexus_name) WHERE vitacomm_name IS NULL'))
    connection.execute(DDL('CREATE UNIQUE INDEX unique_vitacomm ON organization_unit (vitacomm_name) WHERE nexus_name IS NULL'))


class WeeklyStat(Base):
    __tablename__ = "weekly_stat"
    id = Column(Integer, primary_key=True, autoincrement=True)
    residents = Column(Integer, nullable=False)
    residents_with_planned_visits = Column(Integer, nullable=True)
    screen_residents_with_planned_visits = Column(Integer, nullable=True)
    planned_visits = Column(Integer, nullable=True)
    screen_planned_visits = Column(Integer, nullable=True)
    planned_hours = Column(Double, nullable=True)
    screen_planned_hours = Column(Double, nullable=True)
    week = Column(String(8), nullable=False)

    ou_id = Column(Integer, ForeignKey("organization_unit.id"))

    ou = relationship("OU", back_populates="weekly_stats", lazy='subquery')

    __table_args__ = (UniqueConstraint('ou_id', 'week', name='unique_week'),)

    def __repr__(self) -> str:
        return f"Week(id={self.id!r}, OU_id={self.ou_id!r}, week={self.week!r}, residents={self.residents!r})"


class Service(Base):
    __tablename__ = "service"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(60))
    visits = Column(Integer)
    type = Column(String(60))
    week = Column(String(8))

    ou_id = Column(Integer, ForeignKey("organization_unit.id"))

    ou = relationship("OU", back_populates="services", lazy='subquery')

    __table_args__ = (UniqueConstraint('ou_id', 'week', 'name', 'type', name='unique_service'),)

    def __repr__(self) -> str:
        return f"Service(id={self.id!r}, OU_id={self.ou_id!r}, week={self.week!r}, name={self.name!r})"


class Call(Base):
    __tablename__ = "call_log"
    id = Column(String(36), primary_key=True)  # UUID from Vitacomm
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    duration = Column(Time)
    end_reason = Column(String(30))

    callee = Column(String(60))
    callee_cpr = Column(String(11))
    callee_role = Column(String(60))
    callee_ou_id = Column(Integer, ForeignKey("organization_unit.id"))
    callee_ou = relationship("OU", backref="callee_calls", lazy='subquery', foreign_keys=[callee_ou_id])

    caller = Column(String(60))
    caller_cpr = Column(String(11))
    caller_role = Column(String(60))
    caller_ou_id = Column(Integer, ForeignKey("organization_unit.id"))
    caller_ou = relationship("OU", backref="caller_calls", lazy='subquery', foreign_keys=[caller_ou_id])    

    def __repr__(self) -> str:
        return f"Call(id={self.id!r})"
