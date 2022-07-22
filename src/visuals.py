import matplotlib.pyplot as plt
import numpy as np

from src.config_loader import ConfigLoader

simulation_config = ConfigLoader("config/simulation_parameters.yaml")
simulation_parameters = simulation_config.load_config()


class Visuals:
    """
       A class to represent players on a football pitch.

       ...

       Attributes
       ----------
       team : object from Player class
       """
    def __init__(self, team={}):
        self.team = team

    def exact_positions_visual(self):
        """
        Plots the players in their exact positions on the football pitch.

        Returns
        -------
        None
        """
        for player in self.team:
            current_coordinates = self.team[player].current_coordinates
            plt.figure(1)
            plt.scatter(current_coordinates[0], current_coordinates[1], c="r", s=100, alpha=1)
            plt.annotate(player, (current_coordinates[0], current_coordinates[1]))
        plt.title('Exact Player Positions')
        plt.xlim([0, 60])
        plt.ylim([0, 100])
        plt.rcParams["figure.figsize"] = [7.00, 3.50]
        plt.rcParams["figure.autolayout"] = True
        im = plt.imread("assets/football.jpeg")
        plt.imshow(im, extent=[0, 60, 0, 100])
        plt.draw()
        plt.pause(0.0001)
        plt.clf()

    def estimated_positions_visual(self):
        """
        Plots the players in their estimated (calculated using multilateration) positions on the football pitch.

        Returns
        -------
        None
        """
        for player in self.team:
            estimated_coordinates = self.team[player].estimated_coordinates
            plt.figure(2)
            plt.scatter(estimated_coordinates[0], estimated_coordinates[1], c="r", s=100, alpha=1)
            plt.annotate(player, (estimated_coordinates[0], estimated_coordinates[1]))
        plt.title('Estimated Player Positions without Filter')
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
        """
        Plots the velocity profile of a chosen player over the span of the simulation time.

        Returns
        -------
        None
        """
        velocity_magnitude = np.linalg.norm(self.team[player_position].velocity_vector)
        plt.figure(3)
        plt.scatter(time, velocity_magnitude, c="b", s=20, alpha=1)
        plt.title('Velocity Graph for %s Position' % player_position)
        plt.xlabel('Time Elapsed (s)')
        plt.ylabel('Velocity (m/s)')
        #plt.draw()
        #plt.pause(0.0001)

    @staticmethod
    def exact_position_visual(coordinate_vector, time_interval):
        """
        Plots the variation in exact player position of a chosen player over the span of the simulation time.

        Returns
        -------
        None
        """
        plt.figure(4)
        plt.plot(time_interval, coordinate_vector, label=["x", "y"])
        plt.legend()
        plt.title('Exact Position Graph')
        plt.xlabel('Time Elapsed (s)')
        plt.ylabel('Position (m)')
        plt.draw()

    @staticmethod
    def estimated_position_visual(coordinate_vector, time_interval):
        """
        Plots the variation in estimated (calculated using multilateration) player position of a chosen player over the span of the simulation time.
        This plot also shows the applied noise.

        Returns
        -------
        None
        """
        plt.figure(5)
        plt.plot(time_interval, coordinate_vector, label=["x", "y"])
        plt.legend()
        plt.title('Multilateration Position Graph without Filter')
        plt.xlabel('Time Elapsed (s)')
        plt.ylabel('Position (m)')
        plt.draw()

    @staticmethod
    def filter_position_visual(measurements_x, measurements_y, time_interval):
        """
        Plots the variation in estimated (calculated using multilateration) player position of a chosen player over the span of the simulation time.
        Data is plotted after Kalman Filter application.

        Returns
        -------
        None
        """
        plt.figure(6)
        plt.plot(time_interval, np.array(measurements_x), label = 'x')
        plt.plot(time_interval, np.array(measurements_y), label = 'y')
        plt.legend()
        plt.xlabel('Time Elapsed (s)')
        plt.ylabel('Position (m)')
        plt.title('Multilateration Position Graph with Kalman Filter')
        plt.draw()

