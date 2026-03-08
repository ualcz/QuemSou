from sqlalchemy import select, func
from bot.database.connection import db
from bot.models.character import Character

async def add_character(name):
    async with db.async_session() as session:
        async with session.begin():
            result = await session.execute(select(Character).where(Character.name == name))
            if result.scalar_one_or_none():
                return None
            
            new_char = Character(name=name)
            session.add(new_char)
            await session.commit()
            return new_char

async def search_characters(term):
    async with db.async_session() as session:
        query = select(Character.name).where(Character.name.ilike(f"%{term}%")).order_by(Character.name).limit(25)
        result = await session.execute(query)
        return [row[0] for row in result.all()]

async def get_random_characters(count):
    async with db.async_session() as session:
        query = select(Character.name).order_by(func.random()).limit(count)
        result = await session.execute(query)
        return [row[0] for row in result.all()]

async def delete_character(name):
    async with db.async_session() as session:
        async with session.begin():
            result = await session.execute(select(Character).where(Character.name == name))
            char = result.scalar_one_or_none()
            if char:
                await session.delete(char)
                await session.commit()
                return char
            return None
