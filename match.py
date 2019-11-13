from game import Game
from player import Player

class Match:
    def __init__(self, num_players, rl_agent):
        self.num_players = num_players
        self.rl_agent = rl_agent
        self.current_starting_position = 0
        self.playing = True
        self.players = []
        self.games = []

    def start(self):
        for i in range(self.num_players):
            self.players.append(Player(
                position=i,
                is_human=i==0,
                rl_agent=self.rl_agent
            ))

    def run(self):
        while self.playing:
            game = Game(
                match=self,
                starting_position=self.current_starting_position
            )
            game.start()
            game.run()
            game.end()
            self.games.append(game)

    def end(self):
        pass
