"""
Xiang Meng
cs5001 24spring
final project
"""
import random

class GameBoard:
    def __init__(self, name, limited_moves, leaderboard_path):
        self.name = name
        self.limited_moves = limited_moves
        self.move = 0 # Tracks the number of moves by the player.

    def load_puzzle(self, puz_path, tile_clicked, want_shuffle):
        """
        Loads puzzle configuration from a file.
        """
        self.puz_dictionary = {} # Dictionary to store puzzle data.
        with open(puz_path) as file: 
            for i, line in enumerate(file):
                line = line.replace(" ", "")
                line = line.replace("\n", "")
                line = line.split(":")
                if i == 1 or i == 2:
                    # Lines 1 and 2 contain numerical values.
                    self.puz_dictionary[line[0]] = int(line[1])
                elif i >= 4:
                    # Lines after 4 map indices to image paths.
                    self.puz_dictionary[int(line[0])] = line[1]
                else:
                    # The first line contains a string value.
                    self.puz_dictionary[line[0]] = line[1]
        return self.get_puzzle_drawing_information(tile_clicked, want_shuffle)

    def get_puzzle_drawing_information(self, tile_clicked, want_shuffle):
        """
        Resets the move and prepares the tile positions.
        """
        self.move = 0
        # Initialize tile indices in order.
        self.shuffleds = list(range(self.puz_dictionary["number"]))
        if want_shuffle:
            # Shuffle the tiles if requested.
            self.shuffleds = random.sample(
                self.shuffleds, self.puz_dictionary["number"])
        self.blank_index = self.shuffleds.index(max(self.shuffleds))
        xs = []
        ys = []
        img_paths = []
        on_clicks = []
        x_0 = -230
        y_0 = 220
        for i, shuffled in enumerate(self.shuffleds):
            # Calculate grid positions for tiles.
            tile_row, tile_col = divmod(
                i, self.puz_dictionary["number"]**0.5)
            xs.append(x_0+100*tile_col)
            ys.append(y_0-100*tile_row)
            img_paths.append(self.puz_dictionary[shuffled+1])
            # Store click handler for each tile.
            on_clicks.append(
                lambda x, y, var=i: tile_clicked(x, y, var))
        return xs, ys, img_paths, on_clicks

    def can_swap(self, index):
        """
        Determines if the tile at the given index can swap with the blank tile.
        """
        blank_row, blank_col = divmod(
            self.blank_index, self.puz_dictionary["number"]**0.5)
        tile_row, tile_col = divmod(
            index, self.puz_dictionary["number"]**0.5)
        # Tiles can swap if they are adjacent
        return (abs(blank_row - tile_row) == 1 and blank_col == tile_col) or \
               (abs(blank_col - tile_col) == 1 and blank_row == tile_row)

    def swap_tiles(self, index):
        """
        swap operation
        """
        self.move += 1
        # Save current blank and clicked tile indices.
        blank_idx = self.blank_index
        blank_img_path = self.puz_dictionary[self.shuffleds[self.blank_index]+1]
        clicked_img_path = self.puz_dictionary[self.shuffleds[index]+1]
        # Swap the tiles in the shuffleds list.
        self.shuffleds[self.blank_index], self.shuffleds[index] = \
            self.shuffleds[index], self.shuffleds[self.blank_index]
        # Update the blank tile index.
        self.blank_index = index
        return blank_idx, blank_img_path, clicked_img_path

    def check_completion(self):
        """
        Checks if all tiles are in correct positions.
        """
        for i, shuffled in enumerate(self.shuffleds):
            if i is not shuffled:
                return False
        return True

    def check_fail(self):
        """
        Check if the player exceeded the allowed number of moves.
        """
        return self.move >= self.limited_moves
