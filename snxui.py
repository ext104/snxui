#!/bin/python3
import tkinter
import customtkinter
import subprocess
import threading
import time
import psutil
import pystray
from PIL import Image

line_server = ""
line_user = ""
line_pin = ""

icon_image = Image.new('RGB', (16, 16), 'white')
def restore_window(icon, item):
    icon.stop()
    app.deiconify()

def exit_program(icon, item):
    app.quit()

def minimize_to_tray():
    app.withdraw()
    menu = (pystray.MenuItem('Restore', restore_window),
            pystray.MenuItem('Exit', exit_program))
    icon = pystray.Icon("snx_ui", icon_image, "snx ui", menu)
    icon.run()

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")

app = customtkinter.CTk()
app.geometry("800x240")
app.title("snx ui")

label1 = customtkinter.CTkLabel(master=app, text="snx -s")
label1.place(x=150, y=80, anchor=tkinter.CENTER)

entry1 = customtkinter.CTkEntry(master=app)
entry1.place(x=250, y=80, anchor=tkinter.CENTER)
entry1.insert(0, line_server)

label2 = customtkinter.CTkLabel(master=app, text="-u")
label2.place(x=350, y=80, anchor=tkinter.CENTER)

entry2 = customtkinter.CTkEntry(master=app)
entry2.place(x=450, y=80, anchor=tkinter.CENTER)
entry2.insert(0, line_user)

label3 = customtkinter.CTkLabel(master=app, text="pin")
label3.place(x=150, y=120, anchor=tkinter.CENTER)

entry3 = customtkinter.CTkEntry(master=app, show="*")
entry3.place(x=250, y=120, anchor=tkinter.CENTER)
entry3.insert(0, line_pin)

label4 = customtkinter.CTkLabel(master=app, text="token")
label4.place(x=350, y=120, anchor=tkinter.CENTER)

entry4 = customtkinter.CTkEntry(master=app, show="*")
entry4.place(x=450, y=120, anchor=tkinter.CENTER)

status_label = customtkinter.CTkLabel(master=app, text="disconnected")
status_label.place(x=150, y=160, anchor=tkinter.CENTER)

time_label = customtkinter.CTkLabel(master=app, text="")
time_label.place(x=350, y=160, anchor=tkinter.CENTER)

pid_label = customtkinter.CTkLabel(master=app, text="PID: N/A")
pid_label.place(x=550, y=160, anchor=tkinter.CENTER)

def button_function(event=None):
    if button.cget('text') == "connect":
        status_label.configure(text="processing")
        app.update() # update status_label immediately
        try:
            pin_token = entry3.get() + entry4.get()
            command = ['snx', '-s', entry1.get(), '-u', entry2.get()]
            process = subprocess.run(command, input=pin_token, text=True, capture_output=True)
            status_label.configure(text="connected")
            button.configure(text="disconnect")
            start_time = time.time() # start counting time
            threading.Thread(target=timer_function, args=(start_time,)).start() # run timer_function in a new thread
            update_pid() # Update PID
        except:
            status_label.configure(text="failed")
    elif button.cget('text') == "disconnect":
        status_label.configure(text="processing")
        app.update() # update status_label immediately
        try:
            subprocess.check_output(["snx", "-d"])
            status_label.configure(text="disconnected")
            button.configure(text="connect")
            pid_label.configure(text="PID: N/A") # Reset PID
        except:
            status_label.configure(text="failed")
            
def timer_function(start_time):
    while status_label.cget('text') == "connected":
        elapsed_time = time.time() - start_time
        days, rem = divmod(elapsed_time, 86400)
        hours, rem = divmod(rem, 3600)
        minutes, seconds = divmod(rem, 60)
        time_label.configure(text="{:0>2}:{:0>2}:{:0>2}:{:05.2f}".format(int(days), int(hours), int(minutes), seconds))
        app.update()  # Обновляем интерфейс приложения
        time.sleep(0.1)  # Задержка в 0.1 секунды для обновления интерфейса

def update_pid():
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] == 'snx':
            pid_label.configure(text="PID: " + str(proc.info['pid']))
            break

entry4.focus_set()  # Set focus on entry1 to make it active

button = customtkinter.CTkButton(master=app, text="connect", command=button_function)
button.place(x=600, y=120, anchor=tkinter.CENTER) # Adjusted the button placement

minimize_button = customtkinter.CTkButton(master=app, text="minimize", command=minimize_to_tray)
minimize_button.place(x=600, y=80, anchor=tkinter.CENTER) # Placed minimize_button beneath the connect button

app.bind('<Return>', button_function)  # Bind the Enter key to the button_function

app.mainloop()