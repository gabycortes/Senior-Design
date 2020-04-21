import os
import tkinter as tk 
from tkinter import font  as tkfont  
from datetime import date
from datetime import timedelta, datetime
from subprocess import Popen

today = date.today()
today = today.strftime("%m-%d-%y")
file_name = ""


class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        self.title("Cal State LA Baja SAE CVT Test")
        self.geometry("500x500+100+100")

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, InputPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()

    def start_collection(self, running):
        self.show_frame("StartPage")
        global process1
        global process2
        global process3
        if(running):
            process1 = Popen(['python3', 'gps_module_script.py', file_name])
            process2 = Popen(['python3', 'picamera_script.py', file_name])
            process3 = Popen(["sshpass", "-p", "raspberry", "ssh", "pi@169.254.211.228", "python3", "hall_effect_script.py"])
        else:
            process1.terminate()
            process2.terminate()
            process3.terminate()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        lbl_status = tk.Label(self, text="New test run created, ready to begin.")
        lbl_status.grid(row=1, column=0)

        lbl_primarytitle = tk.Label(self, text="Primary RPM")
        lbl_primarytitle.grid(row=2, column=0)

        lbl_secondarytitle = tk.Label(self, text="Secondary RPM")
        lbl_secondarytitle.grid(row=2, column=1)

        # to pass parameters to command use
        # command = lambda: method_name(args)
        btn_start = tk.Button(self, text="Start Test Run", padx=20, command=lambda: controller.show_frame("InputPage"))
        btn_start.grid(row=0, column=0)

        btn_stop = tk.Button(self, text="Stop Test Run", padx=20, command=lambda: controller.start_collection(False))
        btn_stop.grid(row=0, column=1)


class InputPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        lbl_enter_test_type = tk.Label(self, text="Type of test run: ")
        lbl_enter_primary_weight = tk.Label(self, text="CVT primary weight: ")
        lbl_enter_primary_spring = tk.Label(self, text="CVT primary spring: ")
        lbl_enter_secondary_spring = tk.Label(self, text="CVT secondary spring: ")
        lbl_enter_secondary_clock = tk.Label(self, text="CVT secondary clock: ")

        entry_test_type = tk.Entry(self)
        entry_primary_weight = tk.Entry(self)
        entry_primary_spring = tk.Entry(self)
        entry_secondary_spring = tk.Entry(self)
        entry_secondary_clock = tk.Entry(self)

        lbl_enter_test_type.grid(row=0, column=0)
        entry_test_type.grid(row=0, column=1)

        lbl_enter_primary_weight.grid(row=1, column=0)
        entry_primary_weight.grid(row=1, column=1)

        lbl_enter_primary_spring.grid(row=2, column=0)
        entry_primary_spring.grid(row=2, column=1)

        lbl_enter_secondary_spring.grid(row=3, column=0)
        entry_secondary_spring.grid(row=3, column=1)

        lbl_enter_secondary_clock.grid(row=4, column=0)
        entry_secondary_clock.grid(row=4, column=1)

        # create method to save entries before quitting
        btn_ok = tk.Button(self, text="OK", padx=20, command=lambda: self.save_info(entry_test_type.get(),
                                                                                    entry_primary_weight.get(),
                                                                                    entry_primary_spring.get(),
                                                                                    entry_secondary_spring.get(),
                                                                                    entry_secondary_clock.get(),
                                                                                    controller))
        btn_ok.grid(row=5, column=0)

    def save_info(self, type_of_run, primary_weight, primary_spring, secondary_spring, secondary_clock, controller):
        global today

        typeOfRun = type_of_run
        P_Weight = primary_weight
        P_Spring = primary_spring
        S_Spring = secondary_spring
        S_Clock = secondary_clock

        global file
        global file_name
        
        ini_time_for_now = datetime.now()
        current_time = ini_time_for_now.strftime("%H-%M-%S")
        
        file_name = "/media/pi/PI3USB/BajaTest_" + today + "_" + str(current_time)
        file = open(file_name+".csv", "a")

        file.write('Date:,' + str(today) + '\n')
        file.write('Time:,' + str(current_time) + '\n')
        file.write('Test Run Type:,' + str(typeOfRun) + '\n')
        file.write('Primary Weight:,' + str(P_Weight) + '\n')
        file.write('Primary Spring:,' + str(P_Spring) + '\n')
        file.write('Secondary Spring:,' + str(S_Spring) + '\n')
        file.write('Secondary Clock:,' + str(S_Clock) + '\n\n')

        file.close()
        controller.start_collection(True)


class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is page 2", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()


if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()
