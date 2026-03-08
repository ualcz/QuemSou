from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy import text
from bot.config import Config

class Database:
    def __init__(self):
        url = Config.DATABASE_URL
        if not url:
            raise ValueError("DATABASE_URL not found in environment variables")
            
        if url.startswith("postgres://"):
            url = url.replace("postgres://", "postgresql+asyncpg://", 1)
        elif url.startswith("postgresql://"):
            url = url.replace("postgresql://", "postgresql+asyncpg://", 1)
        
        if "?" in url:
            url = url.split("?")[0]
        
        connect_args = {}
        if "neon.tech" in url:
            connect_args["ssl"] = "require"

        self.engine = create_async_engine(
            url,
            connect_args=connect_args,
            echo=False
        )
        self.async_session = async_sessionmaker(
            self.engine, expire_on_commit=False, class_=AsyncSession
        )

    async def connect(self):
        async with self.engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        print("✅ Conectado ao PostgreSQL via SQLAlchemy (Async)")

    async def disconnect(self):
        await self.engine.dispose()

db = Database()
