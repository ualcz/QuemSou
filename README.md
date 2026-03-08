# 🕵️ Quem Sou Eu - Bot para Discord

Bem-vindo ao **Quem Sou Eu**, um bot de jogo interativo para Discord onde o objetivo é adivinhar qual personagem você é, baseado em dicas dadas pelo seu parceiro de jogo!

Este projeto foi desenvolvido em **Python**, utilizando a biblioteca `discord.py` e um sistema de banco de dados robusto com **SQLAlchemy**.

## 🚀 Funcionalidades Principal

- **Modo Dupla**: Jogue com um amigo onde um vê o personagem do outro e ambos devem trocar dicas para adivinhar quem são.
- **Sistema de Ranking**: Ganhe pontos ao adivinhar corretamente e suba no ranking global.
- **Gerenciamento de Personagens**: Administradores podem adicionar e remover personagens facilmente através de comandos slash (`/`).
- **Persistência de Dados**: Seus pontos e perfil são salvos em um banco de dados SQL.

## 🛠️ Tecnologias Utilizadas

- [Python 3.10+](https://www.python.org/)
- [discord.py](https://discordpy.readthedocs.io/)
- [SQLAlchemy](https://www.sqlalchemy.org/) (ORM)
- [PostgreSQL](https://www.postgresql.org/) (Recomendado) ou SQLite para desenvolvimento.
- [Alembic](https://alembic.sqlalchemy.org/) (Migrations)

## 📦 Como Instalar e Rodar

### Pré-requisitos
1. Uma conta no [Discord Developer Portal](https://discord.com/developers/applications) para obter o token do bot.
2. Python instalado em sua máquina.
3. Um banco de dados SQL (ex: PostgreSQL).

### Passos para Configuração

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/ualcz/QuemSou.git
   cd QuemSou
   ```

2. **Crie e ative um ambiente virtual:**
   ```bash
   python -m venv .venv
   # Windows:
   .venv\Scripts\activate
   # Linux/macOS:
   source .venv/bin/activate
   ```

3. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure as variáveis de ambiente:**
   Crie um arquivo `.env` na raiz do projeto com as seguintes chaves:
   ```env
   DISCORD_TOKEN=seu_token_aqui
   DATABASE_URL=postgresql+asyncpg://usuario:senha@localhost/nome_do_banco
   ```

5. **Inicie o bot:**
   ```bash
   python bot/main.py
   ```

## 🎮 Comandos Disponíveis

O bot utiliza **Slash Commands** (`/`) para facilitar a interação.

- `/iniciar_dupla @parceiro`: Inicia uma partida de Quem Sou Eu com outro jogador.
- `/chutar [nome]`: Tente adivinhar quem você é!
- `/desistir`: Abandona a partida atual.
- `/ranking`: Mostra o ranking global de jogadores.
- `/perfil`: Exibe suas estatísticas pessoais.
- `/adicionar_personagem [nome]`: (Apenas Admins) Adiciona um novo personagem à base de dados.
- `/remover_personagem [nome]`: (Apenas Admins) Remove um personagem da base de dados.

## 📁 Estrutura do Projeto

```text
├── bot/
│   ├── commands/      # Cogs do bot (comandos e eventos)
│   ├── database/      # Configurações de conexão ao banco
│   ├── game/          # Lógica principal do jogo
│   ├── models/        # Modelos do SQLAlchemy
│   ├── repositories/  # Acesso aos dados (Query logic)
│   ├── utils/         # Funções utilitárias (Embeds, etc)
│   └── main.py        # Ponto de entrada do bot
├── requirements.txt   # Dependências do projeto
└── README.md          # Este arquivo!
```

