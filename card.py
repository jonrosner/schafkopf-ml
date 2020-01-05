class Card:
    def __init__(self, id, value, color):
        self.id = id
        self.value = value
        self.color = color
        self.playable = True
        self.is_trump = False

    def __str__(self):
        return "[{0}, {1}]".format(self.id, self.is_trump)