import discord
from discord import app_commands
from discord.ext import commands
from bot.repositories import player_repository

class RankingCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="ranking", description="Veja os melhores jogadores")
    async def ranking(self, interaction: discord.Interaction):
        await interaction.response.defer()
        
        top_players = await player_repository.get_ranking(10)
        
        if not top_players:
            await interaction.followup.send("❌ Ninguém jogou ainda!")
            return

        ranking_text = ""
        medals = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]
        
        for i, player in enumerate(top_players):
            ranking_text += f"{medals[i]} **{player['username']}** - `{player['total_points']} pts` ({player['total_wins']} vitórias)\n"

        embed = discord.Embed(
            title="🏆 Ranking Global - Top 10",
            description=ranking_text,
            color=0xFEE75C
        )
        embed.timestamp = discord.utils.utcnow()
        
        await interaction.followup.send(embed=embed)

async def setup(bot):
    await bot.add_cog(RankingCommand(bot))
