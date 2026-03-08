import discord
from discord import app_commands
from discord.ext import commands
from bot.game.game_manager import game_manager

class DesistirCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="desistir", description="Desiste da partida atual e revela os personagens")
    async def desistir(self, interaction: discord.Interaction):
        player_id = str(interaction.user.id)
        game = game_manager.get_active_game(player_id)

        if not game:
            await interaction.response.send_message("❌ Você não está em um jogo ativo.", ephemeral=True)
            return

        await interaction.response.defer()

        is_player1 = game['player1_id'] == player_id
        opponent_id = game['player2_id'] if is_player1 else game['player1_id']

        if is_player1:
            game['player1_guesses'] = 3
            game['player1_score'] = 0
            game['player2_guesses'] = 1
            game['player2_score'] = 5
        else:
            game['player2_guesses'] = 3
            game['player2_score'] = 0
            game['player1_guesses'] = 1
            game['player1_score'] = 5

        await game_manager.finish_game(game['id'], opponent_id)

        reveal_embed = discord.Embed(
            title="🏳️ Fim de Jogo (Desistência)",
            description=f"<@{player_id}> desistiu da partida!",
            color=0xFF0000
        )
        reveal_embed.add_field(name="🎭 Personagens", value=f"<@{game['player1_id']}>: **{game['player1_character']}**\n<@{game['player2_id']}>: **{game['player2_character']}**", inline=False)
        reveal_embed.add_field(name="📊 Pontuação da Partida", value=f"<@{game['player1_id']}>: `{game['player1_score']} pts`\n<@{game['player2_id']}>: `{game['player2_score']} pts`", inline=False)
        reveal_embed.set_footer(text="O desistente teve 3 chutes registrados. O vencedor recebeu +1 chute e 5 pontos.")
        
        await interaction.followup.send(embed=reveal_embed)

async def setup(bot):
    await bot.add_cog(DesistirCommand(bot))
