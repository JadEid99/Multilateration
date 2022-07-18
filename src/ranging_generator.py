import random
from src.position_loader import ConfigLoader

config = ConfigLoader("config/initial_coordinates.yaml")
initial_coordinates = config.load_config()


class Player:
    def __init__(self, position, starting_coordinates = (0, 0), current_coordinates = (0, 0)):
        self.position = position
        self.starting_coordinates = starting_coordinates
        self.current_coordinates = current_coordinates

    def move_player(self):
        self.current_coordinates = (random.randint(0, 61), random.randint(0, 100))

    def assign_coordinates(self):
        self.starting_coordinates = config.load_config()[self.position]

    #def noise_generator(self):


