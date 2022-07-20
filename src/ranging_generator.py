import random
from src.position_loader import ConfigLoader
import numpy as np
import random
import math

player_config = ConfigLoader("config/initial_coordinates.yaml")
simulation_config = ConfigLoader("config/simulation_parameters.yaml")
initial_coordinates = player_config.load_config()
simulation_parameters = simulation_config.load_config()


class Player:
    def __init__(self, position, current_coordinates=(0, 0), velocity_vector=[0, 0]):
        self.position = position
        self.current_coordinates = current_coordinates
        self.velocity_vector = velocity_vector

    def assign_coordinates(self):
        self.current_coordinates = player_config.load_config()[self.position]

    def random_velocity(self):
        average_speed = random.randint(0, 8)  # average football player speed is around 8 m/s

        quadrant1 = simulation_parameters["origin"][0] <= self.current_coordinates[0] <= \
                    simulation_parameters["field_size"][0] / 2 \
                    and simulation_parameters["origin"][1] <= self.current_coordinates[1] <= \
                    simulation_parameters["field_size"][1] / 2  # check if it is in the lower left quadrant of the pitch

        quadrant2 = simulation_parameters["field_size"][0] / 2 <= self.current_coordinates[0] <= \
                    simulation_parameters["field_size"][0] \
                    and simulation_parameters["field_size"][1] / 2 >= self.current_coordinates[1] >= \
                    simulation_parameters["origin"][1]  # check if it is in the lower right quadrant of the pitch

        quadrant3 = simulation_parameters["origin"][0] <= self.current_coordinates[0] <= \
                    simulation_parameters["field_size"][0] / 2 \
                    and simulation_parameters["field_size"][1] / 2 <= self.current_coordinates[1] <= \
                    simulation_parameters["field_size"][1]  # check if it is in the top left quadrant of the pitch

        quadrant4 = simulation_parameters["field_size"][0] / 2 <= self.current_coordinates[0] <= \
                    simulation_parameters["field_size"][0] \
                    and simulation_parameters["field_size"][1] / 2 <= self.current_coordinates[1] <= \
                    simulation_parameters["field_size"][1]  # check if it is in the top right quadrant of the pitch

        if quadrant1:
            movement_trajectory = random.randint(0, 90)
        elif quadrant2:
            movement_trajectory = random.randint(90, 180)
        elif quadrant3:
            movement_trajectory = random.randint(270, 360)
        elif quadrant4:
            movement_trajectory = random.randint(180, 270)
        else:
            average_speed = 0
        self.velocity_vector = [
            float(average_speed * math.cos(movement_trajectory*math.pi/180)), float(average_speed * math.sin(movement_trajectory*math.pi/180))]

    def move_player(self):
        self.random_velocity()
        move_vector = [n * 1 / simulation_parameters["sensor_frequency"] for n in self.velocity_vector]
        self.current_coordinates = [self.current_coordinates[0] + move_vector[0], self.current_coordinates[1] + move_vector[1]]

    # def move_player(self, velocity_vector):

    # def noise_generator(self):
    #     self.current_coordinates = self.current_coordinates + np.random.normal(-0.3, 0.3, 1)
