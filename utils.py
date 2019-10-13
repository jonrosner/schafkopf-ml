class Utils:
    @staticmethod
    def print_players_information(players):
        for player in players:
            print("Player {0}:\n\tCards: {1}".format(player.position, player.cards))