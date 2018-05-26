# import lr_viz
#
# lr = lr_viz.LRViz()
#
# lr.mainloop()

import tensorflow as tf
import numpy as np
from tkinter import *
from dot import Dot
from util import *

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500
DOT_SIZE_RADIUS = 5
x = []
y = []
RUNNING = True


# noinspection PyUnusedLocal
def close(event):
    global RUNNING
    RUNNING = False
    print(RUNNING)


def mouse_l(event):
    ex = event.x
    ey = SCREEN_HEIGHT - event.y
    x.append(normalize(ex, 0, SCREEN_WIDTH))
    y.append(normalize(ey, 0, SCREEN_HEIGHT))
    Dot(canvas, ex, ey, DOT_SIZE_RADIUS)
    text = "(%d, %d)" % (ex, 500 - ey)
    canvas.create_text(ex, 500 - ey - 15, fill="white", text=text, font=("Purisa", 10))


def update():
    pass


window = Tk()
window.resizable(False, False)
window.title("Linear Regression Viz")
window.config(bg="BLACK")
canvas = Canvas(window, bg="black", height=SCREEN_HEIGHT, width=SCREEN_WIDTH, highlightthickness=0)
window.bind("<Button-1>", mouse_l)
window.bind("<Escape>", close)
window.bind("<Destroy>", close)
canvas.pack()
line = canvas.create_line(0, 500, 500, 0, fill="white")

x_data = np.array(x)
y_data = np.array(y)
yPh = tf.placeholder("float")
xPh = tf.placeholder("float")

W = tf.Variable(tf.random_uniform([1], -1.0, 1.0))
b = tf.Variable(tf.zeros([1]))
y_prediction = tf.add(tf.multiply(W, xPh), b)

init = tf.global_variables_initializer()
cost = tf.reduce_mean(tf.square(y_prediction - yPh))
optimizer = tf.train.GradientDescentOptimizer(0.1)
train = optimizer.minimize(cost)
with tf.Session() as sess:
    sess.run(init)
    while RUNNING:
        if len(x) > 0:
            sess.run(train, feed_dict={xPh: np.array(x), yPh: np.array(y)})
            bV = sess.run(b)
            wV = sess.run(W)
            y1 = 500 - float(bV) * 500
            y2 = 500 - ((500 * float(wV)) + (500 * float(bV)))
            canvas.coords(line, 0, y1, 500, y2)
        window.update()
