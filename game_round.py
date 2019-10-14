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

    def start(self):
        print("New round! Player {0} starts.".format(self.starting_position))
        Utils.print_players_information(self.game.match.players)

    def run(self):
        for i in range(self.game.match.num_players):
            current_position = (self.starting_position + i) % self.game.match.num_players
            player = self.game.match.players[current_position]
            picked_card = player.decide_on_card(self)
            print("Player {0} picked card {1}.".format(current_position, str(picked_card)))
            self.played_cards.append(picked_card)
            Rules.set_playable_cards(self, False)

    def end(self):
        self.winner = Rules.calc_round_winner(self)
        print("Player {0} won this round. Played cards: {1}".format(self.winner, " ".join(list(map(str, self.played_cards)))))
        self.game.starting_position = self.winner
        Rules.set_playable_cards(self, True)
        if len(self.game.match.players[0].cards) == 0:
            self.game.playing = False