import discord
from discord import app_commands
from discord.ext import commands
from bot.repositories import player_repository

class PerfilCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="perfil", description="Veja suas estatísticas ou de outro jogador")
    @app_commands.describe(usuario="Usuário que você quer ver o perfil")
    async def perfil(self, interaction: discord.Interaction, usuario: discord.Member = None):
        target = usuario or interaction.user
        await interaction.response.defer()
        
        stats = await player_repository.get_player_stats(str(target.id))
        
        if not stats:
            await interaction.followup.send(f"❌ <@{target.id}> ainda não jogou nenhuma partida!")
            return

        embed = discord.Embed(
            title=f"📊 Perfil de {target.name}",
            color=0x5865F2
        )
        embed.set_thumbnail(url=target.display_avatar.url)
        
        embed.add_field(name="🏆 Vitórias", value=f"`{stats['total_wins']}`", inline=True)
        embed.add_field(name="⭐ Pontos Totais", value=f"`{stats['total_points']}`", inline=True)
        embed.add_field(name="🎮 Partidas", value=f"`{stats['total_games']}`", inline=True)
        
        embed.add_field(name="🎯 Total de Chutes", value=f"`{stats['total_guesses']}`", inline=True)
        embed.add_field(name="📈 Média de Chutes", value=f"`{stats['avg_guesses']}`", inline=True)
        embed.add_field(name="⚡ Eficiência", value=f"`{stats['efficiency_rate']}%`", inline=True)
        
        embed.add_field(name="🔥 Melhor Pontuação", value=f"`{stats['best_score']} pts`", inline=False)
        
        await interaction.followup.send(embed=embed)

async def setup(bot):
    await bot.add_cog(PerfilCommand(bot))
