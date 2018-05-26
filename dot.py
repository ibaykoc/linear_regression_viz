class Dot:
    def __init__(self, canvas, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
        canvas.create_oval(
            x - radius,
            500 - y - radius,
            x + radius,
            500 - y + radius,
            fill="white")
