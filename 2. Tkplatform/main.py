import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import tkinter as tk
from tkinter import ttk
import sys
import os


LARGE_FONT= ("Verdana", 12)


def static_data():
    os.system('python static_data.py')

def rolling_data():
    os.system('python rolling_data.py')

def generate_graph():
    os.system('python Graph.py')



class SeaofBTCapp(tk.Tk):

    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.iconbitmap(self, default="t.ico")
        tk.Tk.wm_title(self, "Auto data platform - TeamCo")
        
        
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, PageOne, PageTwo, PageThree):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()

        
class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="Home Page", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1 = ttk.Button(self, text="Get Static Data",
                            command=lambda: controller.show_frame(PageOne))
        button1.pack()

        button2 = ttk.Button(self, text="Get Rolling Data",
                            command=lambda: controller.show_frame(PageTwo))
        button2.pack()

        button3 = ttk.Button(self, text="Generate Graph",
                            command=lambda: controller.show_frame(PageThree))
        button3.pack()
        
        button3 = ttk.Button(self, text="Exit",
                            command=quit)
        button3.pack()


class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Static Table", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1 = ttk.Button(self, text="Generate static data table",
                            command=static_data)
        button1.pack()

        button2 = ttk.Button(self, text="Back to Home Page",
                            command=lambda: controller.show_frame(StartPage))
        button2.pack()




class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Rolling Data", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1 = ttk.Button(self, text="Generate rolling data table",
                            command=rolling_data)
        button1.pack()

        button2 = ttk.Button(self, text="Back to Home Page",
                            command=lambda: controller.show_frame(StartPage))
        button2.pack()



class PageThree(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Graph Page", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1 = ttk.Button(self, text="Generate graph",
                            command=generate_graph)
        button1.pack()

        button2 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button2.pack()



        

app = SeaofBTCapp()
app.geometry("1280x720")
app.mainloop()