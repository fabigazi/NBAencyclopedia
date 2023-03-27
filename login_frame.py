import tkinter

import customtkinter as ctk
import pymysql
import main_frame

ctk.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

app = ctk.CTk()
app.geometry("350x300")
app.title("CustomTkinter simple_example.py")


def on_closing():
    app.destroy()


app.protocol("WM_DELETE_WINDOW", on_closing)


def button_callback():
    login()


frame = ctk.CTkFrame(master=app)
frame.pack(pady=20, padx=60, fill="both", expand=True)

username = ctk.CTkEntry(master=frame, placeholder_text="Username", )
username.pack(pady=10, padx=10)

password = ctk.CTkEntry(master=frame, placeholder_text="Password")
password.pack(pady=10, padx=10)

login = ctk.CTkButton(master=frame, command=button_callback, text="login")
login.pack(pady=10, padx=10)

cnx = pymysql.connections


def login():
    try:
        global cnx
        cnx = pymysql.connect(host='localhost',
                              user=username.get(),
                              password=password.get(),
                              db='genre',
                              charset='utf8mb4',
                              cursorclass=pymysql.cursors.DictCursor)
    except pymysql.Error:
        tkinter.messagebox.showerror('Login Failure', 'the given information is invalid or connection is not working')
        return

    app.destroy()
    main_frame.run(cnx)


def run():
    app.mainloop()
