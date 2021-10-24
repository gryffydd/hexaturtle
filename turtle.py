"""
Turtle class is to encapsulate the hexagon mapping tool.

It is based on the Logo turtle, but only has 6 facings and moves
one step at a time.
"""

VECTORS = [[0, 2], [1, 1], [1, -1], [0, -2], [-1, -1], [-1, 1]]


class Turtle:
    """The turtle navigates a numpy array of ints."""

    x = 0
    y = 0
    bitmap = None
    facing = 0
    vectors = VECTORS

    def __init__(self, bitmap):
        """Attach the array (world) to the turtle."""
        self.bitmap = bitmap

    def __repr__(self):
        """Print the coordinates and the facing of the turtle."""
        return f"X: {self.x} - Y: {self.y} - F: {self.facing}"

    def place(self, x, y, facing=0):
        """Place the turtle in a specific location in the array."""
        self.x = x
        self.y = y
        self.facing = facing

    def right(self, turns=1):
        """Rotate the turtle right (turns * 60) degrees."""
        self.facing = (self.facing + turns) % len(VECTORS)
        self.facing = (self.facing + len(VECTORS)) % len(VECTORS)
        # TODO test for a VERBOTEN cell to continue turning
        # TODO test for a VIRTUAL cell for pentagons to continue turning

    def left(self, turns=1):
        """Rotate the turtle left 60 degrees."""
        self.right(0 - turns)

    def move(self):
        """Move the turtle to the hexagon that the turtle faces."""
        vx, vy = VECTORS[self.facing]
        self.x += vx
        self.y += vy

    def get_value(self):
        """Get the value in the attached array."""
        return self.bitmap[self.x, self.y]

    def set_value(self, value):
        """Try to set a value in the attached array."""
        try:
            self.bitmap[self.x, self.y] = value
        except TypeError as terr:
            print("Your world is not set properly or you are assigning "
                  "the wrong thing.")
            raise terr
        except IndexError as ierr:
            print("You have moved outside the bounds of the world.")
            raise ierr
        except Exception as err:
            raise err

    def state(self, value):
        """Test the value in the attached array."""
        return self.bitmap[self.x, self.y] == value

    def is_next(self, value):
        """Test the value in the cell the turtle is facing."""
        vx, vy = VECTORS[self.facing]
        return self.bitmap[self.x + vx, self.y + vy] == value

    def is_adjacent(self, value):
        """Test for the value in the turtle's adjacent cells."""
        for vx, vy in VECTORS:
            if self.bitmap[self.x + vx, self.y + vy] == value:
                return True
        return False

    def is_east(self):
        """Test which half of the map the turtle is on in the x-axis."""
        return self.x > (self.bitmap.shape[0] / 2)

    def is_north(self):
        """Test which half of the map the turtle is on in the y-axis."""
        return self.y > (self.bitmap.shape[1] / 2)
