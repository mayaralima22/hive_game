class Player:
    def __init__(self, name, queen, spider, beetle, grasshopper, ant):
        self.hand = {
            queen: 1,
            spider: 2,
            beetle: 2,
            ant: 3,
            grasshopper: 3,
        }

        self.name = name

    def __repr__(self):
        return f"Player('{self.name}')"
    