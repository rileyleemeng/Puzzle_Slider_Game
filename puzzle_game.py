"""
Xiang Meng
cs5001 24spring
final project
"""

from class_ScreenManager import ScreenManager
from class_Gameboard import GameBoard
import glob
from leaderboard import Leaderboard
import datetime
import turtle


class Game:
    def __init__(self):
        self.screen_manager = ScreenManager()
        self.leaderboard = Leaderboard('leaderboard.txt')
        self.screen_manager.show_splash()
        name = self.screen_manager.input_name()
        limited_moves = self.screen_manager.input_numbers_of_moves()
         # Initialize the game board
        self.gameboard = GameBoard(name, limited_moves, self.leaderboard)

        self.screen_manager.draw_square()
        self.screen_manager.draw_status_bar()
        self.screen_manager.draw_sidebar()
        try:
            self.leaderboard.display_scores()
        except FileNotFoundError:
            self.log_error(
                f"Leaderboard file not found: {self.leaderboard.filepath}")
            # Create leaderboard file if not found
            self.leaderboard.createLeaderBoardTxt() 
            self.screen_manager.show_error_image(
                "Resources/leaderboard_error.gif")
            
        # Create buttons
        self.screen_manager.create_button(
            'Resources/resetbutton.gif', (60, -250), self.reset)
        self.screen_manager.create_button(
            'Resources/loadbutton.gif', (150, -250), self.load)
        self.screen_manager.create_button(
            'Resources/quitbutton.gif', (240, -250), self.quit_game)


        puz_files = glob.glob("*.puz")
        if len(puz_files) > 10:
            self.screen_manager.show_error_image(
                'Resources/file_warning.gif')
            puz_files = puz_files[:10] # Limit to the first 10 puzzle files
        elif not puz_files:
            self.screen_manager.show_error_image(
                "Resources/file_error.gif")
        else:
            try:
                xs, ys, img_paths, on_clicks = self.gameboard.load_puzzle(
                    puz_files[0], self.tile_clicked, True)
                self.screen_manager.draw_puzzles(
                    xs, ys, img_paths, on_clicks)
                self.screen_manager.create_thumbnail(
                    self.gameboard.puz_dictionary["thumbnail"])
            except FileNotFoundError as e:
                self.log_error(
                    f"Failed to load puzzle '{puz_files[0]}': {e}")
                self.screen_manager.show_error_image(
                    "Resources/file_error.gif")

    def tile_clicked(self, x, y, index):
        """
        a function to click the tiles.

        Parameters:
            index: the tile index which is clicked by player
        """
        if self.gameboard.can_swap(index):
            blank_index, blank_img_path, clicked_img_path = self.gameboard.swap_tiles(
                index)
            self.screen_manager.update_tiles(
                index, blank_index, clicked_img_path, blank_img_path)
            self.screen_manager.show_move(self.gameboard.move)
            if self.gameboard.check_completion():
                self.leaderboard.write_score(
                    self.gameboard.name, self.gameboard.move)
                self.screen_manager.show_completion()
            if self.gameboard.check_fail():
                self.screen_manager.show_fail()

    def start(self):
        self.screen_manager.screen.mainloop()

    def reset(self, x=None, y=None):
        self.gameboard.move = 0
        self.screen_manager.show_move(0)
        xs, ys, img_paths, on_clicks = self.gameboard.get_puzzle_drawing_information(
            self.tile_clicked, False)
        self.screen_manager.draw_puzzles(xs, ys, img_paths, on_clicks)

    def load(self, x=None, y=None):
        """
            a function to load puzzles files in dictionary
            and logging some errors in error file
        """
        puz_file_paths = glob.glob("*.puz")
        play_puz = self.screen_manager.input_puz(puz_file_paths)
        try:
            xs, ys, imgPaths, on_clicks = self.gameboard.load_puzzle(
                play_puz, self.tile_clicked, True)
            self.screen_manager.create_thumbnail(
                self.gameboard.puz_dictionary["thumbnail"])
            self.screen_manager.draw_puzzles(xs, ys, imgPaths, on_clicks)
        except Exception as e:
            self.log_error(
                f"Failed to load puzzle '{play_puz}': {e}")
            self.screen_manager.show_error_image(
                "Resources/file_error.gif")

    def quit_game(self, x=None, y=None):
        """
            a function to quit game by clicking quit button
        """
        self.screen_manager.show_error_image("Resources/quitmsg.gif")
        turtle.bye()

    def log_error(self, error):
        """
            a funtion to Log message to "mastermind_errors.err"
        """
        with open("5001_puzzle.err", 'a') as error_file:
            error_file.write(f"{datetime.datetime.now()}: {error}\n")

if __name__ == "__main__":
    game = Game()
    game.start()
