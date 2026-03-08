import discord
from discord import app_commands
from discord.ext import commands
from bot.repositories import character_repository

class AdminCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="adicionar_personagem", description="Adiciona um novo personagem ao banco de dados")
    @app_commands.describe(nome="Nome do personagem")
    @app_commands.checks.has_permissions(administrator=True)
    async def adicionar_personagem(self, interaction: discord.Interaction, nome: str):
        await interaction.response.defer()
        
        result = await character_repository.add_character(nome)
        
        if result:
            await interaction.followup.send(f"✅ Personagem **{nome}** adicionado com sucesso!")
        else:
            await interaction.followup.send(f"⚠️ Personagem **{nome}** já existe ou não pôde ser adicionado.")

    @app_commands.command(name="remover_personagem", description="Remove um personagem do banco de dados")
    @app_commands.describe(nome="Nome do personagem")
    @app_commands.checks.has_permissions(administrator=True)
    async def remover_personagem(self, interaction: discord.Interaction, nome: str):
        await interaction.response.defer()
        
        result = await character_repository.delete_character(nome)
        
        if result:
            await interaction.followup.send(f"✅ Personagem **{nome}** removido com sucesso!")
        else:
            await interaction.followup.send(f"❌ Personagem **{nome}** não encontrado.")

    @remover_personagem.autocomplete("nome")
    async def remover_autocomplete(self, interaction: discord.Interaction, current: str):
        choices = await character_repository.search_characters(current)
        return [app_commands.Choice(name=choice, value=choice) for choice in choices]

async def setup(bot):
    await bot.add_cog(AdminCommand(bot))
