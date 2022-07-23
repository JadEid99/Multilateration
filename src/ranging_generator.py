from scipy.optimize import minimize
import numpy as np
import random
import math

from src.config_loader import ConfigLoader


class Player:
    """
       A class to represent players on a football pitch.

       ...

       Attributes
       ----------
       position : str
           player position in football terms
       velocity vector : list of float
           v_x and v_y of the player
       current coordinates : tuple of float
           exact coordinates of player from config file and player movement
       estimated_coordinates: tuple of float
           estimated coordinates of player from multilateration
       """
    def __init__(self, position, velocity_vector=[0, 0], current_coordinates=(0, 0), estimated_coordinates=(0, 0)):

        self.position = position
        self.current_coordinates = current_coordinates
        self.velocity_vector = velocity_vector
        self.estimated_coordinates = estimated_coordinates
        self.initial_coordinates = ConfigLoader("config/initial_coordinates.yaml").load_config()
        self.simulation_parameters = ConfigLoader("config/simulation_parameters.yaml").load_config()

    def assign_coordinates(self):
        """
        Assigns player coordinates from config file.

        Returns
        -------
        None
        """
        self.current_coordinates = self.initial_coordinates[self.position]

    def random_velocity(self):
        """
        Assigns random velocity vector for each player. PLayer movement direction is dependent on current player coordinates.

        Returns
        -------
        None
        """
        average_speed = random.randint(0, 8)  # average football player speed is around 8 m/s

        # Method identifies the quadrant that the player is located in and only allows movement to keep player on the pitch (works to a certain extent).
        quadrant1 = self.simulation_parameters["origin"][0] <= self.current_coordinates[0] <= \
                    self.simulation_parameters["field_size"][0] / 2 \
                    and self.simulation_parameters["origin"][1] <= self.current_coordinates[1] <= \
                    self.simulation_parameters["field_size"][1] / 2  # check if it is in the lower left quadrant of the pitch

        quadrant2 = self.simulation_parameters["field_size"][0] / 2 <= self.current_coordinates[0] <= \
                    self.simulation_parameters["field_size"][0] \
                    and self.simulation_parameters["field_size"][1] / 2 >= self.current_coordinates[1] >= \
                    self.simulation_parameters["origin"][1]  # check if it is in the lower right quadrant of the pitch

        quadrant3 = self.simulation_parameters["origin"][0] <= self.current_coordinates[0] <= \
                    self.simulation_parameters["field_size"][0] / 2 \
                    and self.simulation_parameters["field_size"][1] / 2 <= self.current_coordinates[1] <= \
                    self.simulation_parameters["field_size"][1]  # check if it is in the top left quadrant of the pitch

        quadrant4 = self.simulation_parameters["field_size"][0] / 2 <= self.current_coordinates[0] <= \
                    self.simulation_parameters["field_size"][0] \
                    and self.simulation_parameters["field_size"][1] / 2 <= self.current_coordinates[1] <= \
                    self.simulation_parameters["field_size"][1]  # check if it is in the top right quadrant of the pitch

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
            movement_trajectory = 0
        self.velocity_vector = [
            float(average_speed * math.cos(movement_trajectory * math.pi / 180)),
            float(average_speed * math.sin(movement_trajectory * math.pi / 180))]

    def move_player(self):
        """
        Moves player using the velocity vector.

        Returns
        -------
        None
        """
        move_vector = [n * 1 / self.simulation_parameters["sensor_frequency"] for n in self.velocity_vector]
        self.current_coordinates = [self.current_coordinates[0] + move_vector[0],
                                    self.current_coordinates[1] + move_vector[1]]

    def receiver_distance(self):
        """
        Calcualtes the distance between the player (sensor) and the receivers in each of the corners of the pitch.

        Returns
        -------
        sensor_array: list of floats
        """
        bottom_right_sensor = math.hypot(self.current_coordinates[0] - self.simulation_parameters["bottom_right_corner"][0],
                                         self.current_coordinates[1] - self.simulation_parameters["bottom_right_corner"][1])
        bottom_left_sensor = math.hypot(self.current_coordinates[0] - self.simulation_parameters["origin"][0],
                                        self.current_coordinates[1] - self.simulation_parameters["origin"][1])
        top_right_sensor = math.hypot(self.current_coordinates[0] - self.simulation_parameters["field_size"][0],
                                      self.current_coordinates[1] - self.simulation_parameters["field_size"][1])
        top_left_sensor = math.hypot(self.current_coordinates[0] - self.simulation_parameters["top_left_corner"][0],
                                     self.current_coordinates[1] - self.simulation_parameters["top_left_corner"][1])
        sensor_array = [bottom_left_sensor, bottom_right_sensor, top_left_sensor, top_right_sensor]
        return sensor_array

    @staticmethod
    def noise_generator(sensor_array):
        """
        Applies noise to distance values calculated in previous method.

        Returns
        -------
        sensor_array: list of floats
        """
        return sensor_array + np.random.normal(-0.3, 0.3, 1)

    def multilateration(self):
        """
        Implements the multilateration algorithm that, given the coordinates of the receivers on the corners of the pitch,
        and given their distances to the sensor/player, computes the most probable coordinates of the sensor/player.

        Returns
        -------
        None
        """
        def error(x, c, r):
            return sum([(np.linalg.norm(x - c[i]) - r[i]) ** 2 for i in range(len(c))])

        receiver_coordinates = list(
            np.array([self.simulation_parameters["origin"], self.simulation_parameters["bottom_right_corner"],
                      self.simulation_parameters["top_left_corner"], self.simulation_parameters["field_size"]]))

        distances_to_receiver = self.noise_generator(self.receiver_distance()) # apply noise to receiver signals

        l = len(receiver_coordinates)
        S = sum(distances_to_receiver)
        # compute weight vector for initial guess
        W = [((l - 1) * S) / (S - w) for w in distances_to_receiver]
        # get initial guess of point location
        x0 = sum([W[i] * receiver_coordinates[i] for i in range(l)])
        # optimize distance from signal origin to border of spheres
        self.estimated_coordinates = minimize(error, x0, args=(receiver_coordinates, distances_to_receiver), method='Nelder-Mead').x


class KalmanFilter():
    """
       A class for the KalmanFilter implementation.

       ...

       Attributes
       ----------
       time_interval : list of int
           simulation time
       estiamted_x_coordinates : list of float
           x coordinates returned from multilateration
       estimated_y_coordinates : list of float
           y coordinates returned from multilateration
       F : numpy array
           the state-transition model
       B : numpy array
           is the control-input model which is applied to the control vector
       H : numpy array
           the observation model
       Q : numpy array
           the covariance of the process noise
       R : numpy array
           the covariance of the observation noise
       P : numpy array
       x0 : numpy array
       """
    def __init__(self, time_interval, estimated_x_coordinates, estimated_y_coordinates, F = None, B = None, H = None, Q = None, R = None, P = None, x0 = None):

        if(F is None or H is None):
            raise ValueError("Set proper system dynamics.")

        self.n = F.shape[1]
        self.m = H.shape[1]

        self.time_interval = time_interval
        self.estimated_x_coordinates = estimated_x_coordinates
        self.estimated_y_coordinates = estimated_y_coordinates
        self.F = F
        self.H = H
        self.B = 0 if B is None else B
        self.Q = np.eye(self.n) if Q is None else Q
        self.R = np.eye(self.n) if R is None else R
        self.P = np.eye(self.n) if P is None else P
        self.x = np.zeros((self.n, 1)) if x0 is None else x0

    def predict(self, u = 0):
        self.x = np.dot(self.F, self.x) + np.dot(self.B, u)
        self.P = np.dot(np.dot(self.F, self.P), self.F.T) + self.Q
        return self.x

    def update(self, z):
        y = z - np.dot(self.H, self.x)
        S = self.R + np.dot(self.H, np.dot(self.P, self.H.T))
        K = np.dot(np.dot(self.P, self.H.T), np.linalg.inv(S))
        self.x = self.x + np.dot(K, y)
        I = np.eye(self.n)
        self.P = np.dot(np.dot(I - np.dot(K, self.H), self.P), (I - np.dot(K, self.H)).T) + np.dot(np.dot(K, self.R), K.T)

    def filter(self):
        measurements_x = self.estimated_x_coordinates
        measurements_y = self.estimated_y_coordinates

        predictions_x = []
        predictions_y = []

        for z in measurements_x:
            predictions_x.append(np.dot(self.H,  self.predict())[0])
            self.update(z)

        for z in measurements_y:
            predictions_y.append(np.dot(self.H,  self.predict())[0])
            self.update(z)
        return predictions_x, predictions_y
