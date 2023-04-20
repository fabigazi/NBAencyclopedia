import tkinter as tk
from tkinter import *
from tkinter import messagebox

import customtkinter as ctk
import pymysql
from PIL import Image, ImageTk

from windows.allstar_search import allstar_search
from windows.create_fantasy import open_create_fantasy
from windows.fantasy_search import fantasy_search
from windows.player_search import open_player_search
from windows.team_search import open_team_search


def username_exists(cur, username):
    cur.execute(f"SELECT * FROM user_table WHERE username = '{username}'")
    if cur.fetchall():
        return 1
    else:
        return 0


def on_closing(root):
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        # wn.destroy()
        root.destroy()
        quit


def main_menu(cnx, cur, root, username):
    root.withdraw()

    # Create new window
    wn = Toplevel(root)
    # Create new frame in window
    frame2 = Frame(wn)

    # Set window specifications and location
    window_width = 750
    window_height = 500
    screen_width = wn.winfo_screenwidth()
    screen_height = wn.winfo_screenheight()
    x_coor = screen_width / 2 - window_width / 2
    y_coor = screen_height / 2 - window_height / 2
    wn.geometry("%dx%d+%d+%d" % (window_width, window_height, x_coor, y_coor))

    # Creating widgets
    menu_label = Label(frame2, text='Main Menu', font=('Arial Bold', 32))
    exit_btn = ctk.CTkButton(frame2, text='Exit', font=('Arial', 14),
                             command=lambda: [wn.destroy(), root.deiconify()])
    btn1 = ctk.CTkButton(frame2, text='View / Search Players', font=('Arial', 14),
                         command=lambda: [open_player_search(cnx, cur, root, wn)])
    btn2 = ctk.CTkButton(frame2, text='View / Search Teams', font=('Arial', 14),
                         command=lambda: [open_team_search(cnx, cur, root, wn)])
    btn3 = ctk.CTkButton(frame2, text='View / Search All Star Teams', font=('Arial', 14),
                         command=lambda: [allstar_search(cnx, cur, root, wn)])
    btn4 = ctk.CTkButton(frame2, text='View / Search Fantasy Teams', font=('Arial', 14),
                         command=lambda: [fantasy_search(cnx, cur, root, wn)])
    btn5 = ctk.CTkButton(frame2, text='Create a Team', font=('Arial', 14),
                         command=lambda: [open_create_fantasy(username, cnx, cur, root, wn)])

    # Placing widgets on the screen
    menu_label.grid(row=1, column=0, columnspan=2, sticky='NEWS', pady=(20, 30))
    btn1.grid(row=2, column=0, columnspan=2, sticky='NEWS', padx=20, pady=(10, 10))
    btn2.grid(row=3, column=0, columnspan=2, sticky='NEWS', padx=20, pady=(10, 10))
    btn3.grid(row=4, column=0, columnspan=2, sticky='NEWS', padx=20, pady=(10, 10))
    btn4.grid(row=5, column=0, columnspan=2, sticky='NEWS', padx=20, pady=(10, 10))
    btn5.grid(row=6, column=0, columnspan=2, sticky='NEWS', padx=20, pady=(10, 10))
    exit_btn.grid(row=7, column=0, columnspan=2, sticky='NEWS', padx=20, pady=(10, 10))

    frame2.pack(anchor=tk.CENTER)

    wn.protocol("WM_DELETE_WINDOW", lambda: on_closing(root))
    wn.mainloop()


def login(cnx, cur, root, username, password):
    if not username or not password:
        messagebox.showerror(title='Login Invalid', message='No username or password entered!')

    elif not username_exists(cur, username):
        messagebox.showerror(title='Login Invalid', message='Username does not exist!')

    else:
        cur.execute(f"SELECT * FROM user_table WHERE username = '{username}'")
        user_info = cur.fetchall()

        if user_info[0]['password'] != password:
            messagebox.showerror(title='Login Invalid', message='Incorrect password!')

        else:
            main_menu(cnx, cur, root, username)

    return


def register_confirm(cur, window, first_name, last_name, username, password, password_confirm):
    if not first_name or not last_name or not username or not password or not password_confirm:
        messagebox.showwarning(title='Missing Information', message='Please Ensure All Fields Are Filled')
    elif password != password_confirm:
        messagebox.showerror(title='Invalid Passwords', message='Passwords do not match!')
    else:
        if username_exists(cur, username):
            messagebox.showerror(title='Invalid Username',
                                 message='Username already exists, please select a different one')
        else:
            cur.execute(f"CALL create_username('{username}', '{first_name}', '{last_name}', '{password}')")
            messagebox.showinfo(title='Success!', message='Account successfully created')
            window.destroy()


def register(cur, root):
    # Create new window
    wn = Toplevel(root)

    # Create new frame in window
    frame2 = Frame(wn)

    # Set window specifications and location
    window_width = 500
    window_height = 400
    screen_width = wn.winfo_screenwidth()
    screen_height = wn.winfo_screenheight()
    x_coor = screen_width / 2 - window_width / 2
    y_coor = screen_height / 2 - window_height / 2
    wn.geometry("%dx%d+%d+%d" % (window_width, window_height, x_coor, y_coor))

    # Creating widgets
    create_account_label = ctk.CTkLabel(frame2, text='Create Your Account', font=('Arial Bold', 20))
    first_name_label = ctk.CTkLabel(frame2, text='First Name', font=('Arial', 14))
    first_name_entry = ctk.CTkEntry(frame2)
    last_name_label = ctk.CTkLabel(frame2, text='Last Name', font=('Arial', 14))
    last_name_entry = ctk.CTkEntry(frame2)
    username_label = ctk.CTkLabel(frame2, text='Username', font=('Arial', 14))
    username_entry = ctk.CTkEntry(frame2)
    password_label = ctk.CTkLabel(frame2, text='Password', font=('Arial', 14))
    password_entry = ctk.CTkEntry(frame2, show='*')
    password_confirm_label = ctk.CTkLabel(frame2, text='Confirm Password', font=('Arial', 14))
    password_confirm_entry = ctk.CTkEntry(frame2, show='*')
    create_account_button = ctk.CTkButton(frame2, text='Create Account', font=('Arial', 14),
                                          command=lambda: register_confirm(cur, wn, first_name_entry.get(),
                                                                           last_name_entry.get(),
                                                                           username_entry.get(), password_entry.get(),
                                                                           password_confirm_entry.get()))
    exit_button = ctk.CTkButton(frame2, text='Exit', font=('Arial', 14),
                                command=lambda: wn.destroy())

    # Placing widgets on the screen
    create_account_label.grid(row=1, column=0, columnspan=2, sticky='NEWS', pady=(0, 10))
    first_name_label.grid(row=2, column=0, sticky='W')
    first_name_entry.grid(row=3, column=0, pady=(0, 10))
    last_name_label.grid(row=4, column=0, sticky='W')
    last_name_entry.grid(row=5, column=0, pady=(0, 10))
    username_label.grid(row=6, column=0, sticky='W')
    username_entry.grid(row=7, column=0, pady=(0, 10))
    password_label.grid(row=8, column=0, sticky='W')
    password_entry.grid(row=9, column=0, pady=(0, 10))
    password_confirm_label.grid(row=10, column=0, sticky='W')
    password_confirm_entry.grid(row=11, column=0, pady=(0, 10))
    create_account_button.grid(row=12, column=0, sticky='W', padx=(0, 200))
    exit_button.grid(row=12, column=0, sticky='E')

    frame2.pack(anchor=tk.CENTER)
    return;


def start_screen(cnx, cur, root):
    # Create Frame
    frame = tk.Frame()

    # Creating widgets
    login_label = ctk.CTkLabel(frame, text='Login to your account', font=('Arial Bold', 20))
    username_label = ctk.CTkLabel(frame, text='Username', font=('Arial', 14))
    username_entry = ctk.CTkEntry(frame)
    password_label = ctk.CTkLabel(frame, text='Password', font=('Arial', 14))
    password_entry = ctk.CTkEntry(frame, show='*')
    login_button = ctk.CTkButton(frame, text='Login', font=('Arial', 14),
                                 command=lambda: [login(cnx, cur, root, username_entry.get(), password_entry.get())])
    register_button = ctk.CTkButton(frame, text='Register', font=('Arial', 14),
                                    command=lambda: [register(cur, root), cnx.commit()])
    logo = ImageTk.PhotoImage(Image.open('nba_logo.png'))
    logo_label = tk.Label(frame, image=logo)
    logo_label.image = logo

    # Define a function to clear the Entry Widget Content
    def clear_text():
        username_entry.delete(0, END)
        password_entry.delete(0, END)

    # Placing widgets on the screen
    logo_label.grid(row=0, column=0, columnspan=2, sticky='NEWS')
    login_label.grid(row=1, column=0, columnspan=2, sticky='NEWS', pady=(0, 30))
    username_label.grid(row=2, column=0, sticky='NW')
    username_entry.grid(row=2, column=0, pady=(0, 10))
    password_label.grid(row=4, column=0, sticky='NW')
    password_entry.grid(row=4, column=0, pady=(0, 10))
    login_button.grid(row=6, column=0, sticky='E', pady=(30, 0))
    register_button.grid(row=6, column=0, sticky='W', padx=(0, 200), pady=(30, 0))

    frame.pack(anchor=tk.CENTER)
    root.mainloop()

    return;


def main():
    # connect to database using pymysql
    cnx = pymysql.connect(host='localhost',
                          user='root',
                          password='cs5200PROJECT!',
                          db='nba_app',
                          charset='utf8mb4',
                          cursorclass=pymysql.cursors.DictCursor)

    cur = cnx.cursor()

    root = tk.Tk()
    root.title('NBA Application')

    # Set window specifications and location
    window_width = 500
    window_height = 400
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x_coor = screen_width / 2 - window_width / 2
    y_coor = screen_height / 2 - window_height / 2
    root.geometry("%dx%d+%d+%d" % (window_width, window_height, x_coor, y_coor))
    start_screen(cnx, cur, root)

    # close db connection
    cur.close()
    cnx.close()


if __name__ == "__main__":
    main()
