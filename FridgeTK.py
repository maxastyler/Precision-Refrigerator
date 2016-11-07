#!/usr/bin/env python3
import tkinter as tk
from FridgeClient import *

#Interval with which to update the GUI values
UPDATE_INTERVAL=1000
errors={}
errors[-1]="Connection Error (Is FridgeServer running?)"

class App(tk.Frame):
    def __init__(self, root):
        self.root=root
        super().__init__(root)
        self.init_UI()

    def init_UI(self):
        self.root.title="FridgeTK"
        self.pack(fill=tk.BOTH, expand=True)

        self.grid_rowconfigure(3, weight=1)
        self.grid_columnconfigure(3, weight=1)

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

        self.update_values()

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
        if cur_target_err!=0:
            self.labels['cur_target_val']['text']=errors[-1]
        else:
            self.labels['cur_target_val']['text']=float(cur_target)
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
