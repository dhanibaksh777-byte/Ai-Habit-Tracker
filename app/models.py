from app.database import base
from sqlalchemy import Column,String,Boolean,Integer,DateTime,ForeignKey,Date
from datetime import datetime,timezone
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy import Enum as SQLEnum
from sqlalchemy import Date
from datetime import date as date_type
from sqlalchemy import UniqueConstraint
import enum
import uuid

class HabitStatus(str,enum.Enum):
    DONE = "done"
    SKIPPED = "skipped"

class User(base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4)
    email = Column(String,unique=True,nullable=False)
    username = Column(String,unique=True,nullable=False)
    password = Column(String)
    created_at = Column(DateTime(timezone=True),default=lambda:datetime.now(timezone.utc))
    habits = relationship("Habit",back_populates="owner")

class Habit(base):
    __tablename__ = "habits"
    id = Column(UUID(as_uuid=True),primary_key = True,default=uuid.uuid4)
    name = Column(String(200),nullable=False)
    created_at = Column(DateTime(timezone=True),default=lambda:datetime.now(timezone.utc))
    is_active = Column(Boolean,default=True)
    user_id = Column(ForeignKey("users.id"))
    owner = relationship("User",back_populates="habits")

class HabitLog(base):
    __tablename__ = "habitlogs"
    id = Column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4)
    habit_id = Column(ForeignKey("habits.id"))
    status = Column(SQLEnum(HabitStatus),nullable=False)
    date = Column(Date,default=date_type.today)
    __table_args__ = (
        UniqueConstraint("habit_id", "date", name="uq_habit_date"),
    )

