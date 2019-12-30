from tkinter import *
from datetime import date

def home():

    today = date.today()
    today = today.strftime("%m-%d-%y")

    global file
    global entry_test_type
    global entry_primary_weight
    global entry_primary_spring
    global entry_secondary_spring
    global entry_secondary_clock

    file = open("HEDATA_"+today+".csv", "w+")
    file.write(str(entry_test_type.get())+'\n')
    file.write(str(entry_primary_weight.get())+'\n')
    file.write(str(entry_primary_spring.get())+'\n')
    file.write(str(entry_secondary_spring.get())+'\n')
    file.write(str(entry_secondary_clock.get())+'\n')
    file.close()

    # initial GUI components -------------------------
    root.title("Cal State LA Baja SAE CVT Test")
    root.geometry("500x500+100+100")

    lbl_status = Label(root, text = "New test run created, ready to begin.")
    lbl_status.grid(row = 1, column = 0)

    lbl_primarytitle = Label(root, text = "Primary RPM")
    lbl_primarytitle.grid(row = 2, column = 0)

    lbl_secondarytitle = Label(root, text = "Secondary RPM")
    lbl_secondarytitle.grid(row = 2, column = 1)

    #to pass parameters to command use
    # command = lambda: method_name(args)
    btn_start = Button(root, text="Start Test Run", padx = 20, command =lambda: start(lbl_status))
    btn_start.grid(row = 0, column = 0)

    btn_stop = Button(root, text="Stop Test Run", padx = 20, command =lambda: stop(lbl_status))
    btn_stop.grid(row = 0, column = 1)

def start(lbl):
    lbl.set(text = "Started test run")

def stop(lbl_status):
    lbl_status.config(text = "Stopped test run")

root = Tk()
root.title("New Test Run")

lbl_enter_test_type = Label(root, text = "Type of test run: ")
lbl_enter_primary_weight = Label(root, text = "CVT primary weight: ")
lbl_enter_primary_spring = Label(root, text = "CVT primary spring: ")
lbl_enter_secondary_spring = Label(root, text = "CVT secondary spring: ")
lbl_enter_secondary_clock = Label(root, text = "CVT secondary clock: ")

entry_test_type = Entry(root)
entry_primary_weight = Entry(root)
entry_primary_spring = Entry(root)
entry_secondary_spring = Entry(root)
entry_secondary_clock = Entry(root)

lbl_enter_test_type.grid(row = 0, column = 0)
entry_test_type.grid(row = 0, column = 1)

lbl_enter_primary_weight.grid(row = 1, column = 0)
entry_primary_weight.grid(row = 1, column = 1)

lbl_enter_primary_spring.grid(row = 2, column = 0)
entry_primary_spring.grid(row = 2, column = 1)

lbl_enter_secondary_spring.grid(row = 3, column = 0)
entry_secondary_spring.grid(row = 3, column = 1)

lbl_enter_secondary_clock.grid(row = 4, column = 0)
entry_secondary_clock.grid(row = 4, column = 1)

# create method to save entries before quitting
btn_ok = Button(root, text="OK", padx = 20, command=home)
btn_ok.grid(row = 5, column = 0)

