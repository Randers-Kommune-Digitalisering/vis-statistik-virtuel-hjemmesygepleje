from typing import List
from typing import Optional
from sqlalchemy import Column, ForeignKey, String, Double, Integer, Boolean, DateTime, Uuid, Time
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.schema import UniqueConstraint

class Base(DeclarativeBase):
    pass

class District(Base):
    __tablename__ = "district"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nexus_district =  Column(String(30))
    vitacomm_district = Column(String(30))
    applikator_id = Column(Integer)

    weekly_stats = relationship("WeeklyStat", back_populates="district", cascade="all, delete-orphan")
    services = relationship("Service", back_populates="district", cascade="all, delete-orphan")

    __table_args__ = (UniqueConstraint('nexus_district', 'vitacomm_district', name='unique_district'),)
    
    def __repr__(self) -> str:
        return f"District(id={self.id!r}, nexus={self.nexus_district!r}, vitacomm={self.vitacomm_district!r}, applikator={self.applikator_id!r})"


class WeeklyStat(Base):
    __tablename__ = "weekly_stat"
    id = Column(Integer, primary_key=True, autoincrement=True)
    citizens = Column(Integer)
    citizens_with_planned_visits = Column(Integer)
    screen_citizens_with_planned_visits = Column(Integer)
    planned_visits = Column(Integer)
    screen_planned_visits = Column(Integer)
    planned_hours = Column(Double)
    screen_planned_hours = Column(Double)
    week = Column(String(8))

    district_id = Column(Integer, ForeignKey("district.id"))

    district = relationship("District", back_populates="weekly_stats", lazy='subquery')

    __table_args__ = (UniqueConstraint('district_id', 'week', name='unique_week'),)
    
    def __repr__(self) -> str:
        return f"Week(id={self.id!r}, district={self.district_id!r}, week={self.week!r}, citizens={self.citizens!r})"


class Service(Base):
    __tablename__ = "service"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(60))
    visits = Column(Integer)
    screen = Column(Boolean)
    week = Column(String(8))
    district_id = Column(Integer, ForeignKey("district.id"))

    district = relationship("District", back_populates="services", lazy='subquery')

    __table_args__ = (UniqueConstraint('district_id', 'week', 'name', 'screen', name='unique_service'),)
    
    def __repr__(self) -> str:
        return f"Service(id={self.id!r}, district={self.district_id!r}, week={self.week!r}, name={self.name!r})"
    
class Call(Base):
    __tablename__ = "call_log"
    id = Column(String(36), primary_key=True) #Uuid
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    duration = Column(Time)
    end_reason = Column(String(30))

    callee = Column(String(60))
    callee_employee = Column(Boolean)
    callee_district_id = Column(Integer, ForeignKey("district.id"))
    callee_district = relationship("District", backref="callee_calls", lazy='subquery', foreign_keys=[callee_district_id])

    caller = Column(String(60))
    caller_employee = Column(Boolean)    
    caller_district_id = Column(Integer, ForeignKey("district.id"))
    caller_district = relationship("District", backref="caller_calls", lazy='subquery',foreign_keys=[caller_district_id])    
    
    def __repr__(self) -> str:
        return f"Call(id={self.id!r})"