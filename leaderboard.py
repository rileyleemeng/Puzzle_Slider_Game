"""
Xiang Meng
cs5001 24spring
final project
"""

import turtle
import datetime
from class_ScreenManager import ScreenManager

class Leaderboard:
    def __init__(self, filepath):
        self.filepath = filepath
        self.screen = turtle.Screen()
        self.leaderboard = turtle.Turtle()
        self.setup_display()
        self.screen_manager = ScreenManager()

    def setup_display(self):
        """
        Set up the leaderboard display.
        """
        self.leaderboard.hideturtle()
        self.leaderboard.penup()
        self.leaderboard.speed(0)

    def read_scores(self):
        """
        Read scores from the leaderboard file and return as a sorted list.
        """
        scores = []
        with open(self.filepath, 'r') as file:
            scores = [line.strip().split(" ")
                      for line in file if line.strip()]
        scores = [(name, int(float(steps))) for name, steps in scores]
        # Sort scores by the number of steps
        return sorted(scores, key=lambda x: x[1])

    def createLeaderBoardTxt(self):
        """
        Create a new leaderboard file if it does not exist.
        """
        open(self.filepath, "w").close()

    def display_scores(self):
        """
        Create a new leaderboard file if it does not exist.
        """
        scores = self.read_scores()
        self.leaderboard.clear()
        self.leaderboard.goto(180, 260)
        self.leaderboard.write(
            "Leaders: ", align="left", font=("Arial", 18, "bold"))
        for index, (name, steps) in enumerate(scores[:5]):
            # Move the turtle down for each score
            self.leaderboard.goto(175, 200 - 40 * index)
            self.leaderboard.write(
                f"{index + 1}. {name}: {steps} moves", font=("Arial", 14, "normal"))

    def write_score(self, name, steps):
        """
        Write a new score to the leaderboard file.
        """
        with open(self.filepath, 'a') as file:
            file.write(f"\n{name} {int(steps)}") # Append the new score to the file

    def log_error(self, msg):
        """
        Logs the given message to "5001_puzzle.err"
        """
        with open("5001_puzzle.err", 'a') as error_file:
            # Write the error message with a timestamp
            error_file.write(f"{datetime.datetime.now()}: {msg}\n")
