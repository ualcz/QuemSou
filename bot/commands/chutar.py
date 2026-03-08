import discord
from discord import app_commands
from discord.ext import commands
from bot.game.game_manager import game_manager
from bot.utils import embeds
from bot.repositories import character_repository

class ChutarCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="chutar", description="Tente adivinhar quem você é!")
    @app_commands.describe(personagem="O nome do personagem")
    async def chutar(self, interaction: discord.Interaction, personagem: str):
        player_id = str(interaction.user.id)
        game = game_manager.get_active_game(player_id)

        if not game:
            await interaction.response.send_message("❌ Você não está em uma partida ativa!", ephemeral=True)
            return

        if not game_manager.can_guess(game, player_id):
            is_player1 = game['player1_id'] == player_id
            score = game['player1_score'] if is_player1 else game['player2_score']

            if score > 0:
                await interaction.response.send_message("✅ Você já acertou seu personagem!", ephemeral=True)
            else:
                await interaction.response.send_message("❌ Você já esgotou seus 3 chutes!", ephemeral=True)
            return

        await interaction.response.defer()

        is_player1 = game['player1_id'] == player_id
        secret_char = game['player1_character'] if is_player1 else game['player2_character']

        is_correct = personagem.lower() == secret_char.lower()
        updated_game = await game_manager.process_guess(game['id'], player_id, is_correct)

        if is_correct:
            score = updated_game['player1_score'] if is_player1 else updated_game['player2_score']
            win_embed = embeds.info_embed(
                '🎉 Acertou!',
                f"<@{player_id}> adivinhou corretamente! Era **{secret_char}**!\nVocê ganhou **{score} pontos**."
            )
            await interaction.followup.send(embed=win_embed)
            await self.check_game_end(interaction, updated_game)
        else:
            guesses_used = updated_game['player1_guesses'] if is_player1 else updated_game['player2_guesses']
            remaining = 3 - guesses_used

            fail_embed = embeds.error_embed(
                f"<@{player_id}> errou o chute!\nNão é **{personagem}**.\nVocê ainda tem **{remaining}** tentativas."
            )
            await interaction.followup.send(embed=fail_embed)

            if remaining == 0:
                await interaction.followup.send(f"❌ <@{player_id}> gastou todos os seus 3 chutes!")
                await self.check_game_end(interaction, updated_game)

    @chutar.autocomplete("personagem")
    async def chutar_autocomplete(self, interaction: discord.Interaction, current: str):
        choices = await character_repository.search_characters(current)
        return [app_commands.Choice(name=choice, value=choice) for choice in choices]

    async def check_game_end(self, interaction, game):
        p1_finished = game['player1_score'] > 0 or game['player1_guesses'] >= 3
        p2_finished = game['player2_score'] > 0 or game['player2_guesses'] >= 3

        if p1_finished and p2_finished:
            end_embed = discord.Embed(
                title="🏁 Fim de Jogo!",
                description="Ambos os jogadores terminaram suas tentativas.",
                color=0x00AE86
            )
            end_embed.add_field(name="🎭 Personagens", value=f"<@{game['player1_id']}>: **{game['player1_character']}**\n<@{game['player2_id']}>: **{game['player2_character']}**", inline=False)
            end_embed.add_field(name="🏆 Pontuação Final", value=f"<@{game['player1_id']}>: {game['player1_score']} pts\n<@{game['player2_id']}>: {game['player2_score']} pts", inline=False)
            
            await game_manager.finish_game(game['id'], game['winner_id'])
            await interaction.followup.send(embed=end_embed)

async def setup(bot):
    await bot.add_cog(ChutarCommand(bot))
