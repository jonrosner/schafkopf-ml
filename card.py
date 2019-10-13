class Card:
    def __init_(self, id, value, color):
        self.id = id
        self.value = value
        self.color = color
        self.playable = True
        self.owner_id = -1