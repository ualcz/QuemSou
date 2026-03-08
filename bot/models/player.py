from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer
from bot.models import Base

class Player(Base):
    __tablename__ = "players"

    discord_id: Mapped[str] = mapped_column(String, primary_key=True)
    username: Mapped[str] = mapped_column(String)
    total_wins: Mapped[int] = mapped_column(Integer, default=0)
    total_points: Mapped[int] = mapped_column(Integer, default=0)
    total_games: Mapped[int] = mapped_column(Integer, default=0)
    total_guesses: Mapped[int] = mapped_column(Integer, default=0)
    best_score: Mapped[int] = mapped_column(Integer, default=0)
