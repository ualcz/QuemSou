import discord
from discord import app_commands
from discord.ext import commands
from bot.game.game_manager import game_manager
from bot.utils import embeds
from bot.repositories import player_repository, character_repository

class GameButtons(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Ver Personagem do Parceiro", style=discord.ButtonStyle.primary, emoji="🤫", custom_id="btn_ver_personagem")
    async def ver_personagem(self, interaction: discord.Interaction, button: discord.ui.Button):
        player_id = str(interaction.user.id)
        game = game_manager.get_active_game(player_id)

        if not game:
            await interaction.response.send_message("❌ Você não está em um jogo ativo.", ephemeral=True)
            return

        is_player1 = game['player1_id'] == player_id
        partner_character = game['player2_character'] if is_player1 else game['player1_character']

        embed = embeds.info_embed(
            '🤫 Personagem do Parceiro',
            f"O personagem de seu parceiro é:\n# **{partner_character}**\n\nDê dicas para ele(a) adivinhar! Use `/chutar` para tentar descobrir quem você é."
        )

        await interaction.response.send_message(embed=embed, ephemeral=True)

class IniciarDuplaCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="iniciar_dupla", description="Inicia uma partida de Quem Sou Eu com outra pessoa")
    @app_commands.describe(parceiro="O jogador que vai jogar com você")
    async def iniciar_dupla(self, interaction: discord.Interaction, parceiro: discord.Member):
        await interaction.response.defer(ephemeral=True)
        player1 = interaction.user
        player2 = parceiro

        if player2.bot:
            await interaction.followup.send("❌ Você não pode jogar com um bot!")
            return

        if player1.id == player2.id:
            await interaction.followup.send("❌ Você não pode jogar consigo mesmo!")
            return

        if game_manager.get_active_game(player1.id):
            await interaction.followup.send("❌ Você já está em uma partida ativa!")
            return

        if game_manager.get_active_game(player2.id):
            await interaction.followup.send(f"❌ <@{player2.id}> já está em uma partida ativa!")
            return

        if game_manager.is_channel_occupied(interaction.channel_id):
            await interaction.followup.send("❌ Já existe uma partida em andamento neste canal!")
            return

        try:
            await player_repository.get_or_create_player(str(player1.id), player1.name)
            await player_repository.get_or_create_player(str(player2.id), player2.name)

            characters = await character_repository.get_random_characters(2)
            if len(characters) < 2:
                await interaction.followup.send("❌ Não há personagens suficientes cadastrados no banco de dados!")
                return

            game = await game_manager.create_new_game(
                player1.id,
                player2.id,
                characters[0],
                characters[1],
                interaction.channel_id
            )

            start_embed = embeds.game_start_embed(player1, player2)
            # Send the main message as follow-up (not ephemeral since it's the game start)
            await interaction.channel.send(content=f"<@{player1.id}> <@{player2.id}>", embed=start_embed, view=GameButtons())
            await interaction.followup.send("✅ Partida iniciada!", ephemeral=True)

        except Exception as e:
            print(f"Erro ao iniciar jogo: {e}")
            await interaction.followup.send("❌ Ocorreu um erro ao tentar iniciar a partida.")

async def setup(bot):
    await bot.add_cog(IniciarDuplaCommand(bot))
    bot.add_view(GameButtons())
