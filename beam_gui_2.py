import tkinter as tk 
from tkinter import ttk, font
import requests
import os
import json
import statistics

os.environ['NO_PROXY'] = os.environ['no_proxy'] = '127.0.0.1,localhost,.local'

def submit():
    start_time = start_entry.get()
    end_time = end_entry.get()
    print(start_time, end_time)

    data_dict={"start_logtime":start_time, "end_logtime":end_time}
    print(data_dict)

    r=requests.post(" http://127.0.0.1:5000/diff",data=data_dict)
    json_r=r.json()
    print(json_r)
    print(json_r['data'])

    table_window = tk.Toplevel(root)
    table_window.title("Beam Data")

    style = ttk.Style(table_window)
    style.configure('Treeview', rowheight=30, borderwidth=1, relief="solid")
    style.configure('Treeview.Heading', font=('Courier', 18, 'bold'))
    style.configure('Treeview.Cell', font=('Courier', 16, 'bold'))

    treeview = ttk.Treeview(table_window, columns=('logtime', 'beam_current', 'beam_energy'))
    treeview.heading('logtime', text='Logtime')
    treeview.heading('beam_current', text='Beam Current')
    treeview.heading('beam_energy', text='Beam Energy')
    treeview.pack()

    for item in json_r['data']:
        print(item)
        logtime = str(item['logtime'])
        beam_current = str(item['beam_current'])
        beam_energy = str(item['beam_energy'])
        treeview.insert('', 'end', values=(logtime, beam_current, beam_energy))
    
    #Mean and Standard Deviation
    button_frame = ttk.Frame(table_window)
    button_frame.pack(pady=10)

    def calculate_mean():
        beam_current = 0
        beam_energy = 0
        count = 0
        for item in json_r['data']:
            beam_current +=item['beam_current']
            beam_energy +=item['beam_energy']
            count += 1
        beam_current_mean = beam_current / count
        print(beam_current_mean)
        beam_energy_mean = beam_energy / count
        print(beam_energy_mean)
        mean_label.config(text="Mean of Beam Current = {}\nMean of Beam Energy = {}".format(beam_current_mean, beam_energy_mean))
    
    mean_button = ttk.Button(button_frame, text="Mean", command=calculate_mean)
    mean_button.pack(side="left", padx=10)

    mean_label = ttk.Label(button_frame, text="")
    mean_label.pack(side="left")

    def calculate_stddev():
        beam_current = []
        beam_energy = []
        for item in json_r['data']:
            beam_current.append(item['beam_current'])
            beam_energy.append(item['beam_energy'])
        beam_current_mean = sum(beam_current) / len(beam_current)
        beam_energy_mean = sum(beam_energy) / len(beam_energy)
        beam_current_stddev = statistics.stdev(beam_current, xbar=beam_current_mean)
        print(beam_current_stddev)
        beam_energy_stddev = statistics.stdev(beam_energy, xbar=beam_energy_mean)
        print(beam_energy_stddev)
        stddev_label.config(text="Standard Deviation of Beam Current = {}\nStddev of Beam Energy = {}".format(beam_current_stddev, beam_energy_stddev))

    stddev_button = ttk.Button(button_frame, text="Standard Deviation", command=calculate_stddev)
    stddev_button.pack(side="left", padx=10)

    stddev_label = ttk.Label(button_frame, text="")
    stddev_label.pack(side="left")
        
root = tk.Tk()
root.title("Beam Data")

bold_font = font.Font(family="Courier", size=22, weight="bold")
regular_font = font.Font(family="Courier")

heading_label = tk.Label(root, text="Beam Data", font=bold_font)
heading_label.grid(column=0, row=0, columnspan=2, pady=50, sticky ="WE")

start_label = tk.Label(root, text="Starting Logtime", font=bold_font)
start_label.grid(column=0, row=1, padx=5, pady=20, sticky="W")
start_entry = tk.Entry(root, width=40, font=bold_font)
start_entry.grid(column=1, row=1, padx=5, pady=20)

end_label = tk.Label(root, text="Ending Logtime", font=bold_font)
end_label.grid(column=0, row=2, padx=5, pady=20, sticky="W")
end_entry = tk.Entry(root, width=40, font=bold_font)
end_entry.grid(column=1, row=2, padx=5, pady=20)

submit_button = tk.Button(root, text="Submit", width=20, font=bold_font, command=submit)
submit_button.grid(column=0, row=3, columnspan=2, pady=50)

for child in root.winfo_children():
    child.grid_configure(padx=50)

root.mainloop()