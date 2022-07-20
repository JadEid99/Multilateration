from src.position_loader import ConfigLoader
from src.visuals import Visuals
from src.ranging_generator import Player
import time

player_config = ConfigLoader("config/initial_coordinates.yaml")
simulation_config = ConfigLoader("config/simulation_parameters.yaml")
initial_coordinates = player_config.load_config()
simulation_parameters = simulation_config.load_config()

team = {}
for position in initial_coordinates:
    team[position] = (Player(position))
    team[position].assign_coordinates()

start_time = time.time()
while time.time() < start_time + simulation_parameters["simulation_time"]:
    time.sleep(1/simulation_parameters["sensor_frequency"])
    v1 = Visuals(team)
    v1.positions_visual()
    for position in initial_coordinates:
        team[position].move_player()
