class Box:  # class for sending data to the server and receiving data from the server
    def __init__(self):
        self.client_entity = None
        self.entities = []
        self.hit_hp = 0

    def add_entity(self, entity):
        self.entities.append(entity)

    def add_hit_hp(self, hp: int):
        self.hit_hp += hp
