class Dot:
    def __init__(self, canvas, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
        canvas.create_oval(
            x - radius,
            y - radius,
            x + radius,
            y + radius,
            fill="white")
