"""
Xiang Meng
cs5001 24spring
final project
"""
import turtle
import time

class ScreenManager():
    def __init__(self):
        self.screen = turtle.Screen()
        self.screen.setup(width=700, height=700)
        self.screen.title("Puzzle Slide Game")
        self.drawer = turtle.Turtle()
        self.drawer.speed(10)
        self.drawer.pensize(width=4)
        self.drawer.hideturtle()
        self.show_move_turtle = turtle.Turtle()
        self.show_move_turtle.hideturtle()
        self.show_move_turtle.penup()
        self.thumbnail_turtle = turtle.Turtle()
        self.thumbnail_turtle.hideturtle()
        self.show_move_turtle.goto(-200, -250)
        self.image_turtles = [] # List to hold turtles for each puzzle piece

    def add_shape(self, path, position, on_click):
        """
        create a turtle for it at a specified position with the click event.

        Parameters:
            path: the path added to screen
            position: the location (x, y) added
            on_click: the click event handler
        Return:
            t: turtle instance
        """
        self.screen.addshape(path)
        t = turtle.Turtle(path)
        t.speed(9)
        t.penup()
        t.onclick(on_click)
        t.goto(position)
        return t

    def create_button(self, path, position, on_click):
        """
        Create a button by adding a shape that can be clicked.
        """
        self.add_shape(path, position, on_click)

    def show_splash(self):
        """
        Display the splash screen for 3 seconds and clear it.
        """
        self.screen.bgpic(
            "Resources/splash_screen.gif")
        self.screen.update()
        time.sleep(3)
        self.screen.bgpic("nopic") # Remove the splash screen

    def input_name(self):
        """
        input player name
        """
        return self.screen.textinput("CS5001 Puzzle Slider", "My Name:")

    def input_numbers_of_moves(self):
        """
        input the number of moves they wish to play with
        """
        moves = self.screen.numinput("CS5001 Puzzle Slider - Moves",
                                     "Enter the number pf moves(chances) you want(5-200)?",
                                     5, 5, 200)
        if moves is None or moves < 5 or moves > 200: 
            # if the input is out of the allowed range, input again.
            self.screen.textinput(
                "Error", "Number of moves must be between 5 and 200. Please try again.")
        return moves

    def input_puz(self, puz_paths):
        """
        Prompt the player to choose a puzzle to load.
        """
        return self.screen.textinput("CS5001 Puzzle Slider Load puzzle", puz_paths)

    def show_move(self, move):
        """
        Display the current number of moves the player has made.
        """
        self.show_move_turtle.clear()
        self.show_move_turtle.write(
            "Player Moves:"+str(move), align="left", font=("Arial", 18, "bold"))

    def draw_square(self):
        """
        Draw a large square on the screen to define the play area.
        """
        self.drawer.penup()
        self.drawer.goto(-315, 310)
        self.drawer.pendown()
        self.drawer.forward(450)
        self.drawer.right(90)
        self.drawer.forward(480)
        self.drawer.right(90)
        self.drawer.forward(450)
        self.drawer.right(90)
        self.drawer.forward(480)

    def draw_status_bar(self):
        """
        Draw a status bar at the bottom of the screen.
        """
        self.drawer.penup()
        self.drawer.goto(-315, -200)
        self.drawer.pendown()
        self.drawer.right(90)
        self.drawer.forward(630)
        self.drawer.right(90)
        self.drawer.forward(100)
        self.drawer.right(90)
        self.drawer.forward(630)
        self.drawer.right(90)
        self.drawer.forward(100)

    def draw_sidebar(self):
        """
        Draw a sidebar on the right side of the screen.
        """
        self.drawer.pencolor("blue")
        self.drawer.penup()
        self.drawer.goto(155, 310)
        self.drawer.pendown()
        self.drawer.right(90)
        self.drawer.forward(160)
        self.drawer.right(90)
        self.drawer.forward(480)
        self.drawer.right(90)
        self.drawer.forward(160)
        self.drawer.right(90)
        self.drawer.forward(480)

    def create_thumbnail(self, thumbnail_path):
        """
        Display a thumbnail for the puzzle.
        """
        self.thumbnail_turtle.hideturtle()
        self.thumbnail_turtle = self.add_shape(
            thumbnail_path, (305, 300), None)
        self.thumbnail_turtle.showturtle()

    def draw_puzzles(self, xs, ys, imgPaths, on_clicks):
        """
        Draw all puzzles with images at specified position.
        """
        for image_turtle in self.image_turtles:
            image_turtle.hideturtle()
        self.image_turtles = []
        for x, y, imgPath, on_click in zip(xs, ys, imgPaths, on_clicks):
            self.image_turtles.append(
                self.add_shape(imgPath, (x, y), on_click))

    def update_tiles(self, index, blank_index, clicked_img_path, blank_img_path):
        """
        Update tiles after a move to new positions.
        """
        self.image_turtles[index].shape(blank_img_path)
        self.image_turtles[blank_index].shape(clicked_img_path)

    def show_completion(self):
        """
        Display a completion image when the puzzle is solved.
        """
        completion_turtle = self.add_shape("Resources/winner.gif", (0, 0), None)
        self.screen.update()
        time.sleep(2)
        completion_turtle.hideturtle()

    def show_fail(self):
        """
        Display a failure image when the player fails to complete the puzzle.
        """
        fail_turtle = self.add_shape("Resources/Lose.gif", (0, 0), None)
        self.screen.update()
        time.sleep(2)
        fail_turtle.hideturtle()
        self.show_error_image("Resources/credits.gif")
        turtle.bye()

    def show_error_image(self, path):
        """
        Display an error image to prompt issues.
        """
        self.screen.addshape(path)
        error_turtle = turtle.Turtle(path)
        error_turtle.penup()
        error_turtle.goto(0, 0)
        time.sleep(2)
        error_turtle.hideturtle()
