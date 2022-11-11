from abc import ABCMeta


class Pixel(metaclass=ABCMeta):
    def __init__(self, red: int, green: int, blue: int, alpha: int = 1):
        self.red = red
        self.green = green
        self.blue = blue
        self.alpha = alpha

    def __repr__(self):
        return "Pixel(red={0}, green={1}, blue={2})".format(
            self.red, self.green, self.blue
        )
