import matplotlib.pyplot as plt
import numpy as np
from src.config_loader import ConfigLoader

simulation_config = ConfigLoader("config/simulation_parameters.yaml")
simulation_parameters = simulation_config.load_config()


class Visuals:
    def __init__(self, team={}):
        self.team = team

    def positions_visual(self):
        for player in self.team:
            coordinates = self.team[player].current_coordinates
            plt.figure(1)
            plt.scatter(coordinates[0], coordinates[1], c="r", s=100, alpha=1)
            plt.annotate(player, (coordinates[0], coordinates[1]))
        plt.xlim([0, 60])
        plt.ylim([0, 100])
        plt.rcParams["figure.figsize"] = [7.00, 3.50]
        plt.rcParams["figure.autolayout"] = True
        im = plt.imread("assets/football.jpeg")
        plt.imshow(im, extent=[0, 60, 0, 100])
        plt.draw()
        plt.pause(0.0001)
        plt.clf()

    def velocity_visual(self, player_position="", time=0):
        velocity_magnitude = np.linalg.norm(self.team[player_position].velocity_vector)
        plt.figure(2)
        plt.scatter(time, velocity_magnitude, c="b", s=20, alpha=1)
        plt.title('Velocity Graph for %s Position' % player_position)
        plt.xlabel('Time Elapsed (s)')
        plt.ylabel('Velocity (m/s)')
        plt.draw()
        plt.pause(0.0001)

    @staticmethod
    def position_visual(coordinate_vector, time_interval):
        plt.figure(3)
        plt.plot(time_interval, coordinate_vector)
        plt.title('Position Graph')
        plt.xlabel('Time Elapsed (s)')
        plt.ylabel('Position (m)')
        plt.draw()
        plt.show()

