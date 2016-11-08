#!/usr/bin/env python3
import tkinter as tk
from FridgeClient import *
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
plt.ion()
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
from time import time

#Interval with which to update the GUI values
UPDATE_INTERVAL=1000
errors={}
errors[-1]="Connection Error (Is FridgeServer running?)"


class GraphFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.x_values=[]
        self.y_values=[]
        self.x_t_values=[]
        self.y_t_values=[]
        self.start_time=time()
        self.init_UI()

    def init_UI(self):
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)
        self.f = Figure(figsize=(5,5), dpi=100)
        self.a = self.f.add_subplot(111)
        self.line1,=self.a.plot(self.x_values, self.y_values)
        self.line2,=self.a.plot(self.x_t_values, self.y_t_values)
        self.canvas = FigureCanvasTkAgg(self.f, self)
        self.canvas.show()
        self.canvas.get_tk_widget().grid(row=0, column=0, columnspan=3)
        self.b={}
        self.b['clear']=tk.Button(self, text='Reset', command=self.reset_graph)
        self.b['clear'].grid(row=1, column=0, columnspan=3)

    def update_graph(self):
        self.line1.set_ydata(self.y_values)
        self.line1.set_xdata(self.x_values)
        self.line2.set_ydata(self.y_t_values)
        self.line2.set_xdata(self.x_t_values)
        self.a.relim()
        self.a.autoscale()
        self.f.canvas.draw()

    def reset_graph(self):
        self.y_values.clear()
        self.x_values.clear()
        self.x_t_values.clear()
        self.y_t_values.clear()
        self.start_time=time()
        self.update_graph()

class App(tk.Frame):
    def __init__(self, root):
        self.root=root
        super().__init__(root)
        self.init_UI()
        self.graph_hidden=True

    def init_UI(self):
        self.root.title="FridgeTK"
        self.pack(fill=tk.BOTH, expand=True)

        self.grid_rowconfigure(5, weight=1)
        self.grid_columnconfigure(3, weight=1)

        self.frame1()

        self.update_values()


    def frame1(self):
        self.labels={}

        self.labels['cur_temp_text']=tk.Label(self, text='Current Temperature: ')
        self.labels['cur_temp_text'].grid(row=0, column=0)

        self.labels['cur_temp_val']=tk.Label(self, text='0')
        self.labels['cur_temp_val'].grid(row=0, column=1, columnspan=2)

        self.labels['cur_target_text']=tk.Label(self, text='Current Target Temperature: ')
        self.labels['cur_target_text'].grid(row=1, column=0) 

        self.labels['cur_target_val']=tk.Label(self, text='0')
        self.labels['cur_target_val'].grid(row=1, column=1, columnspan=2)
        self.labels['new_target_text']=tk.Label(self, text='New Target Temperature: ')
        self.labels['new_target_text'].grid(row=2, column=0)
        vcmd = (self.root.register(self.validate),
                    '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
        self.entry=tk.Entry(self, validate="key", validatecommand=vcmd)
        self.entry.grid(row=2, column=1)
        self.button=tk.Button(self, text='Set New Target Temperature', command=self.set_temperature)
        self.button.grid(row=2, column=2)
        self.graph_frame=GraphFrame(self)
        self.graph_frame.grid(row=4, column=0, columnspan=3)
        self.graph_frame.grid_remove()
        self.show_graph=tk.Button(self, text='Show Graph', command=self.toggle_graph)
        self.show_graph.grid(row=3, column=0, columnspan=3)

    def toggle_graph(self):
        if self.graph_hidden:
            self.graph_frame.grid()
        else:
            self.graph_frame.grid_remove()
        self.graph_hidden = not self.graph_hidden
        
    def loop(self):
        self.root.mainloop()

    def set_temperature(self):
        self_temp=self.entry.get()
        try:
            input_num=float(self_temp)
        except:
            input_num=0
        set_temp(input_num)

    def update_values(self):
        cur_temp, cur_temp_err = get_current_temp()  
        cur_target, cur_target_err = get_target_temp()
        if cur_temp_err!=0:
            self.labels['cur_temp_val']['text']=errors[-1]
        else:
            self.labels['cur_temp_val']['text']=float(cur_temp)
            self.graph_frame.x_values.append(time()-self.graph_frame.start_time)
            self.graph_frame.y_values.append(float(cur_temp))
        if cur_target_err!=0:
            self.labels['cur_target_val']['text']=errors[-1]
        else:
            self.labels['cur_target_val']['text']=float(cur_target)
            self.graph_frame.x_t_values.append(time()-self.graph_frame.start_time)
            self.graph_frame.y_t_values.append(float(cur_target))
        self.graph_frame.update_graph()
        self.root.after(UPDATE_INTERVAL, self.update_values)

    def validate(self, action, index, value_if_allowed,
                       prior_value, text, validation_type, trigger_type, widget_name):
        if text in '0123456789.-+ ':
            try:
                if value_if_allowed!='' and value_if_allowed!='-' and value_if_allowed!='.':
                    float(value_if_allowed)
                return True
            except ValueError:
                return False
        else:
            return False

if __name__=='__main__':
    root=tk.Tk()
    app=App(root)
    app.loop()
