from game import Game
from player import Player

class Match:
    def __init__(self, num_players, rl_agent):
        self.num_players = num_players
        self.rl_agent = rl_agent
        self.current_starting_position = 0
        self.playing = True
        self.players = []
        self.game = None

    def start(self):
        for i in range(self.num_players):
            self.players.append(Player(
                position=i,
                is_human=False,
                rl_agent=self.rl_agent
            ))

    def run(self):
        game_no = 0
        while self.playing:
            game = Game(
                match=self,
                starting_position=self.current_starting_position,
                game_no=game_no
            )
            self.game = game
            game.start()
            game.run()
            game.end()
            if game_no % 10000 == 0:
                self.rl_agent.save_networks()
            game_no += 1

    def end(self):
        pass
