import matplotlib.pyplot as plt
from src.ranging_generator import Player
from src.position_loader import ConfigLoader

config = ConfigLoader("config/initial_coordinates.yaml")
initial_coordinates = config.load_config()
team = {}
for position in initial_coordinates:
    team[position] = (Player(position))
    team[position].assign_coordinates()

print(team["LW"].starting_coordinates)

for player in team:
    coordinates = team[player].starting_coordinates
    plt.scatter(coordinates[0], coordinates[1], c="r", s=100, alpha=1)
    plt.annotate(player, (coordinates[0], coordinates[1]))
plt.show()