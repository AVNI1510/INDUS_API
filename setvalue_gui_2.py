import tkinter as tk 
from tkinter import font, ttk
import requests
import os
import json
import statistics

os.environ['NO_PROXY'] = os.environ['no_proxy'] = '127.0.0.1,localhost,.local'

def submit():
    start_logtime = start_entry.get()
    end_logtime = end_entry.get()
    power_supply = power_entry.get()
    print(start_logtime, end_logtime, power_supply)

    data_dict={"start_logtime":start_logtime, "end_logtime":end_logtime, "power_supply":power_supply}

    r=requests.post("http://127.0.0.1:5000/value",data=data_dict)
    json_r=r.json()
    print(json_r['data'])

    table_window = tk.Toplevel(root)
    table_window.title("Set Value")

    style = ttk.Style(table_window)
    style.configure('Treeview', rowheight=30, borderwidth=1, relief="solid")
    style.configure('Treeview.Heading', font=('Courier', 18, 'bold'))
    style.configure('Treeview.Cell', font=('Courier', 16, 'bold'))


    treewview = ttk.Treeview(table_window, columns=('logtime', 'power_supply', 'set_value'))
    treewview.heading('logtime', text='Logtime')
    treewview.heading('power_supply', text='Power Supply Number')
    treewview.heading('set_value', text='Set Value')
    treewview.pack()


    for item in json_r['data']:
        logtime = str(item['Logtime'])
        power_supply = str(item['Power Supply Number'])
        set_value = str(item['Set Value'])
        treewview.insert('', 'end', values=(logtime, power_supply, set_value))

    #Mean and Standard Deviation
    button_frame = ttk.Frame(table_window)
    button_frame.pack(pady=10)

    def calculate_mean():
        set_value = 0
        count = 0
        for item in json_r['data']:
            set_value += item['Set Value']
            count += 1
        set_value_mean = set_value / count
        print(set_value_mean)
        mean_label.config(text="Mean of Set Values = {}".format(set_value_mean))
            
    mean_button = ttk.Button(button_frame, text="Mean", command=calculate_mean)
    mean_button.pack(side="left", padx=10)

    mean_label = ttk.Label(button_frame, text="")
    mean_label.pack(side="left")

    def calculate_stddev():
        set_value = []
        for item in json_r['data']:
            set_value.append(item['Set Value'])
        set_value_mean = sum(set_value) / len(set_value)
        set_value_stddev = statistics.stdev(set_value, xbar=set_value_mean)
        print(set_value_stddev)
        sttdev_label.config(text="Standard Deviation of Set Values = {} ".format(set_value_stddev))
    
    sttdev_button =ttk.Button(button_frame, text="Standard Deviation", command=calculate_stddev)
    sttdev_button.pack(side="left", padx=10)

    sttdev_label = ttk.Label(button_frame, text="")
    sttdev_label.pack(side="left")

root = tk.Tk()
root.title("Set Value")

bold_font = font.Font(family="Courier", size=22, weight="bold")
regular_font = font.Font(family="Courier")

heading_label = tk.Label(root, text="Set Value of Power Supply", font=bold_font)
heading_label.grid(column=0, row=0, columnspan=2, pady=50, sticky ="WE")

start_label = tk.Label(root, text="Starting Logtime", font=bold_font)
start_label.grid(column=0, row=1, padx=5, pady=20, sticky="W")
start_entry = tk.Entry(root, width=40, font=bold_font)
start_entry.grid(column=1, row=1, padx=5, pady=20)

end_label = tk.Label(root, text="Ending Logtime", font=bold_font)
end_label.grid(column=0, row=2, padx=5, pady=20, sticky="W")
end_entry = tk.Entry(root, width=40, font=bold_font)
end_entry.grid(column=1, row=2, padx=5, pady=20)

power_label = tk.Label(root, text="Power Supply Number", font=bold_font)
power_label.grid(column=0, row=3, padx=5, pady=20, sticky="W")
power_entry = tk.Entry(root, width=40, font=bold_font)
power_entry.grid(column=1, row=3, padx=5, pady=20)

submit_button = tk.Button(root, text="Submit", width=20, font=bold_font, command=submit)
submit_button.grid(column=0, row=4, columnspan=2, pady=50)

for child in root.winfo_children():
    child.grid_configure(padx=50)

root.mainloop()
