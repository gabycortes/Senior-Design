# os.system('python3 ../Desktop/simplecameratest.py')
from tkinter import *
import time
import os

running = True  # Global flag
idx = 0  # loop index


def start():
    """Enable scanning by setting the global flag to True."""
    global running
    running = True


def stop():
    """Stop scanning by setting the global flag to False."""
    global running
    running = False


root = Tk()
root.title("Greatest GUI Ever")
root.geometry("500x500+300+300")

app = Frame(root)
app.grid()

start = Button(app, text="Start Scan", command=start)
stop = Button(app, text="Stop", command=stop)

start.grid()
stop.grid()

while True:
    if idx % 500 == 0:
        root.update()

    if running:
        time.sleep(3)  # amount of time before another picture is taken
        os.system('python3 simplecameratest.py')
        # idx += 1
        # print(f"{idx}")
