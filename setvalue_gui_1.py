import tkinter as tk 
from tkinter import messagebox, font
import requests
import os
import json
from tkinter import ttk

os.environ['NO_PROXY'] = os.environ['no_proxy'] = '127.0.0.1,localhost,.local'

def submit():
    logtime = start_entry.get()
    power_supply = power_entry.get()
    print(logtime, power_supply)

    data_dict={"logtime":logtime, "power_supply":power_supply}

    r=requests.post("http://127.0.0.1:5000/set",data=data_dict)
    json_r=r.json()
    print(json_r['data'])

    table_window = tk.Toplevel(root)
    table_window.title("Set Value")

    style = ttk.Style(table_window)
    style.configure('Treeview', rowheight=50, borderwidth=1, relief="solid")
    style.configure('Treeview.Heading', font=('Courier', 18, 'bold'))
    style.configure('Treeview.Cell', font=('Courier', 16, 'bold'))

    treeview = ttk.Treeview(table_window, columns=('logtime', 'power_supply', 'set_value'))
    treeview.heading('logtime', text='Logtime')
    treeview.heading('power_supply', text='Power Supply')
    treeview.heading('set_value', text='Set Value')
    treeview.pack()

    for item in json_r['data']:
        print(item)
        logtime = str(item['Logtime'])
        power_supply = str(item['Power Supply Number'])
        set_value = str(item['Set Value'])
        treeview.insert('', 'end', values=(logtime, power_supply, set_value))

root = tk.Tk()
root.title("Set Value")

bold_font = font.Font(family="Courier", size=22, weight="bold")
regular_font = font.Font(family="Courier")

heading_label = tk.Label(root, text="Set Value of Power Supply", font=bold_font)
heading_label.grid(column=0, row=0, columnspan=2, pady=50, sticky ="WE")

start_label = tk.Label(root, text="Logtime", font=bold_font)
start_label.grid(column=0, row=1, padx=5, pady=20, sticky="W")
start_entry = tk.Entry(root, width=40, font=bold_font)
start_entry.grid(column=1, row=1, padx=5, pady=20)

power_label = tk.Label(root, text="Power Supply Number", font=bold_font)
power_label.grid(column=0, row=3, padx=5, pady=20, sticky="W")
power_entry = tk.Entry(root, width=40, font=bold_font)
power_entry.grid(column=1, row=3, padx=5, pady=20)

submit_button = tk.Button(root, text="Submit", width=20, font=bold_font, command=submit)
submit_button.grid(column=0, row=4, columnspan=2, pady=50)

for child in root.winfo_children():
    child.grid_configure(padx=50)

root.mainloop()