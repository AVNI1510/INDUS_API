import tkinter as tk 
from tkinter import ttk, font
import requests
import os 
import json

os.environ['NO_PROXY'] = os.environ['no_proxy'] = '127.0.0.1,localhost,.local'

def submit():
    logtime = start_entry.get()
    print (logtime)
    
    data_dict={"logtime":logtime}
  
    r=requests.post("http://127.0.0.1:5000/output",data=data_dict)
    json_r=r.json()
    print(json_r)
    print(json_r['key'])

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

    for item in json_r['key']:
        logtime = str(item['logtime'])
        beam_current = str(item['beam_current'])
        beam_energy = str(item['beam_energy'])
        treeview.insert('', 'end', values=(logtime, beam_current, beam_energy))

root = tk.Tk()
root.title("Beam Data")

bold_font = font.Font(family="Courier", size=22, weight="bold")
regular_font = font.Font(family="Courier")

heading_label = tk.Label(root, text="Beam Data", font=bold_font)
heading_label.grid(column=0, row=0, columnspan=2, pady=50, sticky ="WE")

start_label = tk.Label(root, text="Logtime", font=bold_font)
start_label.grid(column=0, row=1, padx=5, pady=20, sticky="W")
start_entry = tk.Entry(root, width=40, font=bold_font)
start_entry.grid(column=1, row=1, padx=5, pady=20)

submit_button = tk.Button(root, text="Submit", font=bold_font, width=20, command=submit)
submit_button.grid(column=0, row=3, columnspan=2, pady=50)

for child in root.winfo_children():
    child.grid_configure(padx=50)

root.mainloop()