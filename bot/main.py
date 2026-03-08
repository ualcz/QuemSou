import discord
from discord.ext import commands
import os
from bot.config import Config
from bot.database.connection import db

class OMMQBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.members = True
        intents.message_content = True
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        await db.connect()
        
        # Load Cogs from the commands directory
        commands_dir = os.path.join(os.path.dirname(__file__), 'commands')
        for filename in os.listdir(commands_dir):
            if filename.endswith('.py') and filename != '__init__.py':
                cog_name = f'bot.commands.{filename[:-3]}'
                try:
                    await self.load_extension(cog_name)
                    print(f"✅ Cog carregado: {cog_name}")
                except Exception as e:
                    print(f"❌ Erro ao carregar cog {cog_name}: {e}")

    async def on_ready(self):
        print(f'✅ Bot logado como {self.user} (ID: {self.user.id})')
        print('------')
        
    async def close(self):
        await db.disconnect()
        await super().close()

bot = OMMQBot()

@bot.command()
@commands.is_owner()
async def sync(ctx):
    await bot.tree.sync()
    await ctx.send("Comandos sincronizados!")

def run():
    if not Config.TOKEN:
        print("❌ Token não encontrado no arquivo .env")
    else:
        bot.run(Config.TOKEN)

if __name__ == "__main__":
    run()
