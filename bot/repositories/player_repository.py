from sqlalchemy import select, update, func, text, Numeric
from bot.database.connection import db
from bot.models.player import Player

async def get_or_create_player(discord_id, username):
    async with db.async_session() as session:
        async with session.begin():
            result = await session.execute(select(Player).where(Player.discord_id == str(discord_id)))
            player = result.scalar_one_or_none()
            
            if player:
                player.username = username
            else:
                player = Player(discord_id=str(discord_id), username=username)
                session.add(player)
            
            await session.commit()
            return player

async def get_player_stats(discord_id):
    async with db.async_session() as session:
        avg_guesses = func.round(func.cast(Player.total_guesses, Numeric) / Player.total_games, 1)
        efficiency = func.round((func.cast(Player.total_points, Numeric) / (Player.total_games * 5)) * 100, 1)

        query = select(
            Player.discord_id,
            Player.username,
            Player.total_wins,
            Player.total_points,
            Player.total_games,
            Player.total_guesses,
            Player.best_score,
            func.coalesce(avg_guesses, 0).label("avg_guesses"),
            func.coalesce(efficiency, 0).label("efficiency_rate")
        ).where(Player.discord_id == str(discord_id))
        
        result = await session.execute(query)
        row = result.mappings().first()
        return row

async def get_ranking(limit=10):
    async with db.async_session() as session:
        avg_guesses = func.round(func.cast(Player.total_guesses, Numeric) / Player.total_games, 1)
        efficiency = func.round((func.cast(Player.total_points, Numeric) / (Player.total_games * 5)) * 100, 1)

        query = select(
            Player.discord_id,
            Player.username,
            Player.total_wins,
            Player.total_points,
            Player.total_games,
            Player.total_guesses,
            Player.best_score,
            func.coalesce(avg_guesses, 0).label("avg_guesses"),
            func.coalesce(efficiency, 0).label("efficiency_rate")
        ).where(Player.total_games > 0).order_by(
            Player.total_points.desc(), 
            Player.total_wins.desc()
        ).limit(limit)
        
        result = await session.execute(query)
        return result.mappings().all()

async def update_player_stats(player_id, guesses, score, is_win):
    async with db.async_session() as session:
        async with session.begin():
            query = update(Player).where(Player.discord_id == str(player_id)).values({
                Player.total_wins: Player.total_wins + (1 if is_win else 0),
                Player.total_points: Player.total_points + score,
                Player.total_games: Player.total_games + 1,
                Player.total_guesses: Player.total_guesses + guesses,
                Player.best_score: func.greatest(Player.best_score, score)
            })
            await session.execute(query)
            await session.commit()
