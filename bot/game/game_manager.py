import time
from datetime import datetime
from bot.repositories import player_repository

class GameManager:
    def __init__(self):
        self.active_games = {}

    async def create_new_game(self, player1_id, player2_id, char1, char2, channel_id):
        game_id = str(int(time.time() * 1000))
        game = {
            'id': game_id,
            'player1_id': str(player1_id),
            'player2_id': str(player2_id),
            'player1_character': char1,
            'player2_character': char2,
            'player1_guesses': 0,
            'player2_guesses': 0,
            'player1_score': 0,
            'player2_score': 0,
            'winner_id': None,
            'channel_id': str(channel_id),
            'status': 'active',
            'created_at': datetime.now()
        }
        self.active_games[game_id] = game
        return game

    def get_game(self, game_id):
        return self.active_games.get(game_id)

    def get_active_game(self, player_id):
        player_id = str(player_id)
        for game in self.active_games.values():
            if game['status'] == 'active' and (game['player1_id'] == player_id or game['player2_id'] == player_id):
                return game
        return None

    def is_channel_occupied(self, channel_id):
        channel_id = str(channel_id)
        for game in self.active_games.values():
            if game['status'] == 'active' and game['channel_id'] == channel_id:
                return True
        return False

    async def process_guess(self, game_id, player_id, is_correct):
        player_id = str(player_id)
        game = self.active_games.get(game_id)
        if not game:
            return None

        is_player1 = game['player1_id'] == player_id
        current_guesses = game['player1_guesses'] if is_player1 else game['player2_guesses']

        if is_player1:
            game['player1_guesses'] += 1
        else:
            game['player2_guesses'] += 1

        if is_correct:
            points = 0
            if current_guesses == 0: points = 5
            elif current_guesses == 1: points = 3
            elif current_guesses == 2: points = 1

            # Penalidade se já houver um vencedor
            if game['winner_id'] and game['winner_id'] != player_id:
                points = max(0, points - 1)
            elif not game['winner_id']:
                game['winner_id'] = player_id

            if is_player1:
                game['player1_score'] = points
            else:
                game['player2_score'] = points

        return game

    async def finish_game(self, game_id, winner_id):
        game = self.active_games.get(game_id)
        if not game:
            return

        players = [
            {'id': game['player1_id'], 'guesses': game['player1_guesses'], 'score': game['player1_score']},
            {'id': game['player2_id'], 'guesses': game['player2_guesses'], 'score': game['player2_score']}
        ]

        for p in players:
            is_win = p['id'] == str(winner_id)
            await player_repository.update_player_stats(p['id'], p['guesses'], p['score'], is_win)

        if game_id in self.active_games:
            del self.active_games[game_id]

    def can_guess(self, game, player_id):
        if not game:
            return False
        player_id = str(player_id)
        is_player1 = game['player1_id'] == player_id
        guesses = game['player1_guesses'] if is_player1 else game['player2_guesses']
        score = game['player1_score'] if is_player1 else game['player2_score']

        return score == 0 and guesses < 3

game_manager = GameManager()
