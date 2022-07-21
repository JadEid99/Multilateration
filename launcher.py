from src.config_loader import ConfigLoader
from src.visuals import Visuals
from src.ranging_generator import Player
import time
import matplotlib.pyplot as plt
import numpy

player_config = ConfigLoader("config/initial_coordinates.yaml")
simulation_config = ConfigLoader("config/simulation_parameters.yaml")
initial_coordinates = player_config.load_config()
simulation_parameters = simulation_config.load_config()

team = {}
for position in initial_coordinates:
    team[position] = (Player(position))
    team[position].assign_coordinates()

N_start = 0
start_time = time.time()
movement = []
time_interval = []
while time.time() < start_time + simulation_parameters["simulation_time"]: # simulation runtime set in configuration file
    N = round((time.time()-start_time)/simulation_parameters["change_direction"])
    time.sleep(1/simulation_parameters["sensor_frequency"]) # frequency set in configuration file to simulate sensor refresh rate
    v1 = Visuals(team)
    v1.positions_visual()
    v1.velocity_visual("RB", time.time()-start_time)
    if N_start != N:
        for position in initial_coordinates:
            team[position].random_velocity()
        N_start = N
    for position in initial_coordinates:
        team[position].move_player()
        movement.append(team["RB"].current_coordinates[0])
        time_interval.append(time.time()-start_time)

v1.position_visual(movement, time_interval)

