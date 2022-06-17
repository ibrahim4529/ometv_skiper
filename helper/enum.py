from enum import Enum

class HandlePosition(Enum):
    """
    Enum for the handle of the position of frame widget.
    """
    TOP_LEFT = 0
    TOP_MIDDLE = 1
    TOP_RIGHT = 2
    MIDDLE_LEFT = 3
    MIDDLE = 4
    MIDDLE_RIGHT = 5
    BOTTOM_LEFT = 6
    BOTTOM_MIDDLE = 7
    BOTTOM_RIGHT = 8
    NO_HANDLE = 9

class DegrePosition(Enum):
    """
    Enum for the degree of the arrow button for spesific position.
    """
    TOP_MIDDLE = 0
    TOP_RIGHT = 45
    MIDDLE_RIGHT = 90
    BOTTOM_RIGHT = 135
    BOTTOM_MIDDLE = 180
    BOTTOM_LEFT = 225
    MIDDLE_LEFT = 270
    TOP_LEFT = 315