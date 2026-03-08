from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer
from bot.models import Base

class Character(Base):
    __tablename__ = "characters"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, unique=True)
