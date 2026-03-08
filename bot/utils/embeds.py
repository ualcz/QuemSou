import discord
from bot.config import Config

def info_embed(title, description):
    embed = discord.Embed(
        title=title,
        description=description,
        color=Config.INFO_COLOR
    )
    return embed

def error_embed(description):
    embed = discord.Embed(
        title="❌ Erro",
        description=description,
        color=Config.ERROR_COLOR
    )
    return embed

def success_embed(title, description):
    embed = discord.Embed(
        title=title,
        description=description,
        color=Config.SUCCESS_COLOR
    )
    return embed

def game_start_embed(player1, player2):
    embed = discord.Embed(
        title="🎮 Partida Iniciada!",
        description=f"Um novo jogo começou entre **{player1.name}** e **{player2.name}**!",
        color=Config.PRIMARY_COLOR
    )
    embed.add_field(name="Como jogar?", value="Você deve descobrir quem você é fazendo perguntas ao seu parceiro.\nEle(a) pode ver o SEU personagem, e você o DELE(A).\n\nUse os botões/comandos abaixo:", inline=False)
    embed.add_field(name="`/chutar`", value="Tente adivinhar seu personagem (Máximo 3 tentativas).", inline=True)
    embed.add_field(name="`/desistir`", value="Sair da partida e revelar os personagens.", inline=True)
    embed.set_footer(text="Dica: Clique no botão abaixo para ver o personagem do seu parceiro.")
    return embed
