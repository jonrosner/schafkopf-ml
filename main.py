from match import Match

def init():
    num_players = 4
    match = Match(num_players)
    match.start()
    match.run()
    match.end()

if __name__ == '__main__':
    init()