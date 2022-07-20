import matplotlib.pyplot as plt
from src.ranging_generator import Player


class Visuals:
    def __init__(self, team={}):
        self.team = team

    def positions_visual(self):
        for player in self.team:
            coordinates = self.team[player].current_coordinates
            plt.scatter(coordinates[0], coordinates[1], c="r", s=100, alpha=1)
            plt.annotate(player, (coordinates[0], coordinates[1]))
        plt.xlim([0, 60])
        plt.ylim([0, 100])
        plt.rcParams["figure.figsize"] = [7.00, 3.50]
        plt.rcParams["figure.autolayout"] = True
        im = plt.imread("assets/football.jpeg")
        plt.imshow(im, extent=[0, 60, 0, 100])
        plt.draw()
        plt.pause(0.1)
        plt.clf()
