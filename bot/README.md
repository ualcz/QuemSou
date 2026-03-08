# 🤖 Bot "Quem Sou Eu" - Detalhes Técnicos

Este diretório contém o coração do bot. Abaixo estão detalhes técnicos sobre a arquitetura e fluxos de jogo para desenvolvedores.

## 🏗️ Arquitetura

O bot segue uma arquitetura modular inspirada em padrões de **Domain Driven Design (DDD)** simplificado:

1. **Commands (Cogs)**: Localizados em `bot/commands/`, são as interfaces do usuário do bot. Cada arquivo é um `Cog` do `discord.py`.
2. **Game Manager**: Localizado em `bot/game/game_manager.py`, é um **Singleton** que gerencia o estado das partidas ativas em memória.
3. **Repositories**: Localizados em `bot/repositories/`, encapsulam a lógica de persistência de dados. Interagem diretamente com o banco de dados.
4. **Models**: Localizados em `bot/models/`, definem os esquemas do SQLAlchemy (Tabelas: `players`, `characters`).
5. **Database Connection**: Localizada em `bot/database/connection.py`, gerencia a sessão assíncrona do SQLAlchemy.

## 🔄 Fluxo de Jogo

O fluxo típico de uma partida é:

1. **Início**: O comando `/iniciar_dupla` é enviado.
2. **Verificações**: O bot verifica se os jogadores ou o canal já estão ocupados em outras partidas.
3. **Sorteio**: O `character_repository` busca dois personagens aleatórios no banco de dados.
4. **Criação**: O `game_manager` cria um objeto de jogo em memória para salvar o estado da partida atual.
5. **Interação**: Jogadores usam botões integrados nas mensagens para enviar dicas ou o comando `/chutar` para adivinhar.
6. **Fim**: Quando um jogador acerta, o bot calcula os pontos baseados nas configurações em `bot/config.py` e encerra a partida no `game_manager`.

## 💾 Banco de Dados

O bot utiliza **SQLAlchemy 2.0+** com suporte assíncrono.

### Tabelas Principais:
- **`players`**: Armazena `discord_id`, `name`, `points`, `wins`, `losses`.
- **`characters`**: Armazena apenas o `id` e o `name` dos personagens que podem ser sorteados.

## ⚙️ Configurações

As constantes do bot e cálculos de pontos estão centralizados em `bot/config.py`. Isso permite ajustar facilmente o equilíbrio do jogo sem mexer na lógica principal.

```python
# Exemplo de configuração em bot/config.py
POINTS_BASE = 5         # Pontos base por acerto
POINTS_DECREMENT = 2    # Redução por erros subsequentes
```

## 🛠️ Como contribuir com o Código

Para adicionar um novo comando:
1. Crie um novo arquivo `.py` em `bot/commands/`.
2. Herde de `commands.Cog`.
3. Defina seus comandos slash com `@app_commands.command`.
4. O bot carregará automaticamente o novo arquivo ao iniciar (veja `bot/main.py`).

---

*Para dúvidas técnicas, abra uma Issue ou entre em contato com os desenvolvedores.*
