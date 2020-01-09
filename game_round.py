from rules import Rules
from utils import Utils

class Game_round:
    def __init__(self,
        game,
        starting_position):
        self.game = game
        self.starting_position = starting_position
        self.played_cards = []
        self.winner = None
        self.round_points = 0

    def start(self):
        #print("New round! Player {0} starts.".format(self.starting_position))
        #Utils.print_players_information(self.game.match.players)
        pass

    def run(self):
        for i in range(self.game.match.num_players):
            current_position = (self.starting_position + i) % self.game.match.num_players
            player = self.game.match.players[current_position]
            picked_card = player.decide_on_card(self)
            self.game.log_msgs.append("Player {0} picked card {1}.".format(current_position, str(picked_card)))
            self.played_cards.append(picked_card)
            Rules.set_playable_cards(self, False)

    def end(self):
        self.winner = Rules.calc_round_winner(self)
        self.round_points = Rules.calc_round_points(self)
        self.game.match.players[self.winner].game_points += self.round_points
        self.game.log_msgs.append("Player {0} won this round. Points: {1}. Played cards: {2}".format(self.winner, list(map(lambda player: player.game_points, self.game.match.players)), " ".join(list(map(str, self.played_cards)))))
        self.game.starting_position = self.winner
        Rules.set_playable_cards(self, True)
        self.game.played_cards += self.played_cards
        if len(self.game.match.players[0].cards) == 0:
            self.game.playing = False