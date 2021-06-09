class Occupied(Exception):
    def __str__(self):
        return 'This cell is occupied! Choose another one!'


class NotNum(Exception):
    def __str__(self):
        return 'You should enter numbers!'


class CoordinatesRange(Exception):
    def __str__(self):
        return 'Coordinates should be from 1 to 3!'


class BadParameters(Exception):
    def __str__(self):
        return 'Bad parameters!'
