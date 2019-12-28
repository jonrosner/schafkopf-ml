from match import Match
from rl_agent import Rl_Agent

def init():
    num_players = 3
    rl_agent = Rl_Agent()
    match = Match(num_players, rl_agent)

    match.start()
    match.run()
    match.end()

if __name__ == '__main__':
    init()
