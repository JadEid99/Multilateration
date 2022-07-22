import matplotlib.pyplot as plt
import numpy as np

from src.config_loader import ConfigLoader
from src.visuals import Visuals
from src.ranging_generator import Player, KalmanFilter


# Configuration loading for initial player positions and simulation parameters from config files
player_config = ConfigLoader("config/initial_coordinates.yaml")
simulation_config = ConfigLoader("config/simulation_parameters.yaml")
initial_coordinates = player_config.load_config()
simulation_parameters = simulation_config.load_config()


def main(animation=False, tracked_position="LW"):
    team = {}
    for position in initial_coordinates:
        team[position] = (Player(position))
        team[position].assign_coordinates()

    N_start = 0
    exact_movement = []
    estimated_movement = []
    estimated_x_movement = []
    estimated_y_movement = []
    time_interval = []

    for i in range(simulation_parameters["simulation_time"]*simulation_parameters["sensor_frequency"]):
        N = round(i/(simulation_parameters["change_direction"]*simulation_parameters["sensor_frequency"]))
        v1 = Visuals(team)
        if N_start != N:
            for position in initial_coordinates: # Assigning random velocity to each player defined within the configuration (velocity is randomized after predefined time interval)
                team[position].random_velocity()
            N_start = N
        for position in initial_coordinates:
            team[position].move_player() # moves player on pitch using the assigned velocity
            team[position].multilateration() # calculates player position using multilateration
            exact_movement.append(team[tracked_position].current_coordinates)
            time_interval.append(i/simulation_parameters["sensor_frequency"])
            estimated_x_movement.append(team[tracked_position].estimated_coordinates[0])
            estimated_y_movement.append(team[tracked_position].estimated_coordinates[1])
            estimated_movement.append(team[tracked_position].estimated_coordinates)

        if animation:
            v1.exact_positions_visual()
            v1.estimated_positions_visual()

    dt = 1/simulation_parameters["sensor_frequency"]
    kf = KalmanFilter(time_interval, estimated_x_movement, estimated_y_movement, F = np.array([[1, dt, 0], [0, 1, dt], [0, 0, 1]]), H = np.array([1, 0, 0]).reshape(1, 3),
                      Q = np.array([[0.05, 0.05, 0.0], [0.05, 0.05, 0.0], [0.0, 0.0, 0.0]]), R = np.array([0.5]).reshape(1, 1)) # Applying kalman filter to multilateration data
    filtered_x, filtered_y = kf.filter()
    v1.filter_position_visual(filtered_x, filtered_y, time_interval)
    v1.estimated_position_visual(estimated_movement, time_interval)
    v1.exact_position_visual(exact_movement, time_interval)
    plt.show()


if __name__ == '__main__':
    animation = input("View live animation of players on pitch (Might impact performance)? (Answer with True/False)")
    tracked_position = input("Position to view posistion data (refer to readme/config for possible positions): ")
    main(animation, tracked_position)

