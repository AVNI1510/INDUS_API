import tkinter as tk 
from tkinter import ttk, font
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

    r=requests.post("http://127.0.0.1:5000/data", data=data_dict)
    json_r=r.json()
    print(json_r['data'])

    table_window = tk.Toplevel(root)
    table_window.title("Readback Value")

    style = ttk.Style(table_window)
    style.configure('Treeview', rowheight=30, borderwidth=1, relief="solid")
    style.configure('Treeview.Heading', font=('Courier', 18, 'bold'))
    style.configure('Treeview.Cell', font=('Courier', 16, 'bold'))

    treeview = ttk.Treeview(table_window, columns=('logtime', 'power_supply', 'readback_value'))
    treeview.heading('logtime', text='Logtime')
    treeview.heading('power_supply', text='Power Supply')
    treeview.heading('readback_value', text='Readback Value')
    treeview.pack()

    for item in json_r['data']:
        logtime = str(item['Logtime'])
        power_supply = str(item['Power Supply Number'])
        readback_value = str(item['Readback Value'])
        treeview.insert('','end', values=(logtime, power_supply, readback_value))

    #Mean and Standard Deviation
    button_frame = ttk.Frame(table_window)
    button_frame.pack(pady=10)

    def calculate_mean():
        readback_value = 0
        count = 0
        for item in json_r['data']:
            readback_value += item['Readback Value']
            count += 1
        readback_value_mean = readback_value / count
        print(readback_value_mean)
        mean_label.config(text="Mean of Readback Values = {}".format(readback_value_mean))
            
    mean_button = ttk.Button(button_frame, text="Mean", command=calculate_mean)
    mean_button.pack(side="left", padx=10)

    mean_label = ttk.Label(button_frame, text="")
    mean_label.pack(side="left")

    def calculate_stddev():
        readback_value = []
        for item in json_r['data']:
            readback_value.append(item['Readback Value'])
        readback_value_mean = sum(readback_value) / len(readback_value)
        readback_value_stddev = statistics.stdev(readback_value, xbar=readback_value_mean)
        print(readback_value_stddev)
        sttdev_label.config(text="Standard Deviation of Readback Values = {} ".format(readback_value_stddev))
    
    sttdev_button =ttk.Button(button_frame, text="Standard Deviation", command=calculate_stddev)
    sttdev_button.pack(side="left", padx=10)

    sttdev_label = ttk.Label(button_frame, text="")
    sttdev_label.pack(side="left")

root = tk.Tk()
root.title("Readback Value")

bold_font = font.Font(family="Courier", size=22, weight="bold")
regular_font = font.Font(family="Courier")

heading_label = tk.Label(root, text="Readback Value of Power Supply", font=bold_font)
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