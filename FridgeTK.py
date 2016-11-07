import tkinter as tk
from FridgeClient import *

def validate_text(*args):
    print(args)
    return False

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

        labels={}

        labels['cur_temp_text']=tk.Label(self, text='Current Temperature: ')
        labels['cur_temp_text'].grid(row=0, column=0)

        labels['cur_temp_val']=tk.Label(self, text='0')
        labels['cur_temp_val'].grid(row=0, column=1, columnspan=2)

        labels['cur_target_text']=tk.Label(self, text='Current Target Temperature: ')
        labels['cur_target_text'].grid(row=1, column=0) 

        labels['cur_target_val']=tk.Label(self, text='0')
        labels['cur_target_val'].grid(row=1, column=1, columnspan=2)
        labels['new_target_text']=tk.Label(self, text='New Target Temperature: ')
        labels['new_target_text'].grid(row=2, column=0)
        vcmd = (self.root.register(self.validate),
                    '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
        entry=tk.Entry(self, validate="key", validatecommand=vcmd)
        entry.grid(row=2, column=1)
        button=tk.Button(self, text='Set New Target Temperature', command=lambda: print("HI"))
        button.grid(row=2, column=2)

    def loop(self):
        self.root.mainloop()

    def validate(self, action, index, value_if_allowed,
                       prior_value, text, validation_type, trigger_type, widget_name):
        if text in '0123456789.-+ ':
            try:
                if value_if_allowed!='':
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
