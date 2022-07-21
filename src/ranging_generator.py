from scipy.optimize import minimize
from src.config_loader import ConfigLoader
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
            float(average_speed * math.cos(movement_trajectory * math.pi / 180)),
            float(average_speed * math.sin(movement_trajectory * math.pi / 180))]

    def move_player(self):
        move_vector = [n * 1 / simulation_parameters["sensor_frequency"] for n in self.velocity_vector]
        self.current_coordinates = [self.current_coordinates[0] + move_vector[0],
                                    self.current_coordinates[1] + move_vector[1]]

    def receiver_distance(self):
        bottom_right_sensor = math.hypot(self.current_coordinates[0] - simulation_parameters["bottom_right_corner"][0],
                                         self.current_coordinates[1] - simulation_parameters["bottom_right_corner"][1])
        bottom_left_sensor = math.hypot(self.current_coordinates[0] - simulation_parameters["origin"][0],
                                        self.current_coordinates[1] - simulation_parameters["origin"][1])
        top_right_sensor = math.hypot(self.current_coordinates[0] - simulation_parameters["field_size"][0],
                                      self.current_coordinates[1] - simulation_parameters["field_size"][1])
        top_left_sensor = math.hypot(self.current_coordinates[0] - simulation_parameters["top_left_corner"][0],
                                     self.current_coordinates[1] - simulation_parameters["top_left_corner"][1])
        sensor_array = [bottom_left_sensor, bottom_right_sensor, top_left_sensor, top_right_sensor]
        return sensor_array

    @staticmethod
    def noise_generator(sensor_array):
        return sensor_array + np.random.normal(-0.3, 0.3, 1)

    def multilateration(self):
        def error(x, c, r):
            return sum([(np.linalg.norm(x - c[i]) - r[i]) ** 2 for i in range(len(c))])

        receiver_coordinates = list(
            np.array([simulation_parameters["origin"], simulation_parameters["bottom_right_corner"],
                      simulation_parameters["top_left_corner"], simulation_parameters["field_size"]]))

        distances_to_receiver = self.noise_generator(self.receiver_distance()) # apply noise to receiver signals

        l = len(receiver_coordinates)
        S = sum(distances_to_receiver)
        # compute weight vector for initial guess
        W = [((l - 1) * S) / (S - w) for w in distances_to_receiver]
        # get initial guess of point location
        x0 = sum([W[i] * receiver_coordinates[i] for i in range(l)])
        # optimize distance from signal origin to border of spheres
        return minimize(error, x0, args=(receiver_coordinates, distances_to_receiver), method='Nelder-Mead').x

    #def handle_noise(self):

