# os.system('python3 ../Desktop/simplecameratest.py')
from tkinter import *
import os
from subprocess import Popen

running = True  # Global flag
idx = 0  # loop index


def start():
    """Enable scanning by setting the global flag to True."""
    global running
    # os.system('python3 /Users/bowenwaugh/Documents/GA/GA_Puzzles/simple.py')
    global process
    process = Popen(['python3', '/Users/bowenwaugh/Documents/GA/GA_Puzzles/simple.py'])
    running = True


def stop():
    """Stop scanning by setting the global flag to False."""
    global running
    running = False
    root.destroy()


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

    # if running:
    #     idx += 1
    #     print(f"{idx}")
