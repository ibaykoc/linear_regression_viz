import tkinter as tk
from tkinter import ttk

LARGE_FONT = ("Verdana", 12)


class LRViz(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        w, h = self.winfo_screenwidth(), self.winfo_screenheight()
        self.geometry("%dx%d+0+0" % (w - 100, h - 100))
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        frame = StartPage(master=container)

        self.frames[StartPage] = frame

        frame.grid(row=0, column=0, sticky='NSEW')

        self.show_frame(StartPage)

    def show_frame(self, frame_to_show):
        frame = self.frames[frame_to_show]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, **kw):
        super().__init__(**kw)
        canvas = Cartesian(master=self, bg="black", highlightthickness=0)
        canvas.pack()


class Cartesian(tk.Canvas):
    x_line_pad_bottom = 40
    x_min_length = 5
    x_max_length = 100
    x_length = 10
    x_single_indicator_length = 10
    x_single_indicators = []
    x_single_indicator_labels = []
    x_single_indicator_label_font = ("Purisa", 10)
    x_indicator_value_offset = 10
    x_grids = []
    x_grid_color = "gray15"
    x_cartesian_line_color = "blue"

    y_line_pad_left = 40
    y_min_length = 5
    y_max_length = 100
    y_length = 10
    y_single_indicator_length = 10
    y_single_indicators = []
    y_single_indicator_labels = []
    y_single_indicator_label_font = ("Purisa", 10)
    y_indicator_value_offset = 10
    y_grids = []
    y_grid_color = "gray15"
    y_cartesian_line_color = "green"

    def __init__(self, **kw):
        super().__init__(**kw)
        self.height = 0
        self.width = 0
        # Create x grid line system
        self.x_line = self.create_line(
            10,
            self.y_to_drawing_coord(self.x_line_pad_bottom),
            self.width - 10,
            self.y_to_drawing_coord(self.x_line_pad_bottom),
            fill=self.x_cartesian_line_color
        )
        for i in range(self.x_length):
            grid = self.create_line(0, 0, 0, 0, fill=self.x_grid_color)
            self.x_grids.append(grid)
            label = self.create_text(
                0,
                0,
                fill="white",
                text=(i + 1) * self.x_indicator_value_offset,
                font=self.x_single_indicator_label_font
            )
            self.x_single_indicator_labels.append(label)
            line = self.create_line(0, 0, 0, 0, fill="white")
            self.x_single_indicators.append(line)

        # Create y grid line system
        self.y_line = self.create_line(
            self.y_line_pad_left,
            self.y_to_drawing_coord(0),
            self.y_line_pad_left,
            self.y_to_drawing_coord(self.height),
            fill="green"
        )
        for i in range(self.y_length):
            grid = self.create_line(0, 0, 0, 0, fill=self.y_grid_color)
            self.y_grids.append(grid)
            label = self.create_text(
                0,
                0,
                fill="white",
                text=(i + 1) * self.y_indicator_value_offset,
                font=self.y_single_indicator_label_font
            )
            self.y_single_indicator_labels.append(label)
            line = self.create_line(0, 0, 0, 0, fill="white")
            self.y_single_indicators.append(line)

        x_length_slider = tk.Scale(self, from_=self.x_min_length, to=self.x_max_length, orient="horizontal",
                                   command=self.update_x_length)
        x_length_slider.set(10)
        y_length_slider = tk.Scale(self, from_=self.y_min_length, to=self.y_max_length, orient="vertical",
                                   command=self.update_y_length)
        y_length_slider.set(10)
        self.create_window(100, 450, anchor="s", window=x_length_slider)
        self.create_window(450, 450, anchor="s", window=y_length_slider)
        self.master.bind("<Configure>", self.on_parent_resize)

    def update_x_length(self, value=None):
        diff = self.x_length - int(value)
        if diff < 0:
            for i in range(abs(diff)):
                grid = self.create_line(0, 0, 0, 0, fill=self.x_grid_color)
                self.x_grids.append(grid)
                label = self.create_text(
                    0,
                    0,
                    fill="white",
                    text=(i + 1) * self.x_indicator_value_offset,
                    font=self.x_single_indicator_label_font
                )
                self.x_single_indicator_labels.append(label)
                line = self.create_line(0, 0, 0, 0, fill="white")
                self.x_single_indicators.append(line)
        self.x_length = int(value)
        self.update_x_indicator()

    def update_y_length(self, value=None):
        diff = self.y_length - int(value)
        if diff < 0:
            for i in range(abs(diff)):
                grid = self.create_line(0, 0, 0, 0, fill=self.y_grid_color)
                self.y_grids.append(grid)
                label = self.create_text(
                    0,
                    0,
                    fill="white",
                    text=(i + 1) * self.y_indicator_value_offset,
                    font=self.y_single_indicator_label_font
                )
                self.y_single_indicator_labels.append(label)
                line = self.create_line(0, 0, 0, 0, fill="white")
                self.y_single_indicators.append(line)
        self.y_length = int(value)
        self.update_y_indicator()

    def update_x_indicator(self):
        self.coords(
            self.x_line,
            0,
            self.y_to_drawing_coord(self.x_line_pad_bottom),
            self.width,
            self.y_to_drawing_coord(self.x_line_pad_bottom)
        )
        i = 1
        for line in self.x_single_indicators:
            x = ((self.width - self.y_line_pad_left) / self.x_length * i) + self.y_line_pad_left
            y_bot = self.y_to_drawing_coord(self.x_line_pad_bottom - self.x_single_indicator_length / 2)
            y_top = self.y_to_drawing_coord(self.x_line_pad_bottom + self.x_single_indicator_length / 2)

            self.coords(line, x, y_bot, x, y_top)
            self.coords(self.x_single_indicator_labels[i - 1], x, y_bot + 15)
            self.itemconfig(self.x_single_indicator_labels[i - 1], text=i * self.x_indicator_value_offset)
            self.coords(self.x_grids[i - 1], x, 0, x, self.height)

            i += 1

    def update_y_indicator(self):
        self.coords(
            self.y_line,
            self.y_line_pad_left,
            0,
            self.y_line_pad_left,
            self.height
        )
        i = 1
        for line in self.y_single_indicators:
            y = self.y_to_drawing_coord(
                ((self.height - self.x_line_pad_bottom) / self.y_length * i) + self.x_line_pad_bottom
            )
            x_left = self.y_line_pad_left - self.y_single_indicator_length / 2
            x_right = self.y_line_pad_left + self.y_single_indicator_length / 2

            self.coords(line, x_left, y, x_right, y)
            self.coords(self.y_single_indicator_labels[i - 1], x_left - 15, y)
            self.itemconfig(self.y_single_indicator_labels[i - 1], text=i * self.y_indicator_value_offset)
            self.coords(self.y_grids[i - 1], 0, y, self.width, y)

            i += 1

    def on_parent_resize(self, event):
        self.height = event.height
        self.width = event.width
        self.config(width=self.width, height=self.height)
        self.update_x_indicator()
        self.update_y_indicator()

    def y_to_drawing_coord(self, val):
        return self.height - val
