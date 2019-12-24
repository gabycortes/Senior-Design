from tkinter import *

def start():
    global lbl_status
    lbl_status.config(text = "Starting test run")
    createNew = Tk()
    createNew.title("New Test Run")

    lbl_enter_test_type = Label(createNew, text = "Type of test run: ")
    lbl_enter_primary_weight = Label(createNew, text = "CVT primary weight: ")
    lbl_enter_primary_spring = Label(createNew, text = "CVT primary spring: ")
    lbl_enter_secondary_spring = Label(createNew, text = "CVT secondary spring: ")
    lbl_enter_secondary_clock = Label(createNew, text = "CVT secondary clock: ")

    entry_test_type = Entry(createNew)
    entry_primary_weight = Entry(createNew)
    entry_primary_spring = Entry(createNew)
    entry_secondary_spring = Entry(createNew)
    entry_secondary_clock = Entry(createNew)
    # entry.get() saves the text
    
    lbl_enter_test_type.grid(row = 0, column = 0)
    entry_test_type.grid(row = 0, column = 1)
    
    lbl_enter_primary_weight.grid(row = 1, column = 0)
    entry_primary_weight.grid(row = 1, column = 1)

    lbl_enter_secondary_spring.grid(row = 2, column = 0)
    entry_secondary_spring.grid(row = 2, column = 1)

    lbl_enter_secondary_clock.grid(row = 3, column = 0)
    entry_secondary_clock.grid(row = 3, column = 1)

    # create method to save entries before quitting
    btn_ok = Button(createNew, text="OK", padx = 20, command=createNew.destroy)
    btn_ok.grid(row = 4, column = 0)
    

def stop():
    # needs troubleshooting
    global root
    global lbl_status
    lbl_status.config(text = "Stopped test run")



# initial GUI components -------------------------
root = Tk()
root.title("Cal State LA Baja SAE CVT Test")
root.geometry("500x500+100+100")

#to pass parameters to command use
# command = lambda: method_name(args)
btn_start = Button(root, text="Start Test Run", padx = 20, command=start)
btn_start.grid(row = 0, column = 0)

btn_stop = Button(root, text="Stop Test Run", padx = 20, command = stop)
btn_stop.grid(row = 0, column = 1)

lbl_status = Label(root, text = "")
lbl_status.grid(row = 1, column = 0)

lbl_primarytitle = Label(root, text = "Primary RPM")
lbl_primarytitle.grid(row = 2, column = 0)

lbl_secondarytitle = Label(root, text = "Secondary RPM")
lbl_secondarytitle.grid(row = 2, column = 1)

root.mainloop()
