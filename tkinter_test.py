import pymysql
import tkinter as tk
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk

from window import Window
from window_template import open_window


def username_exists(cur, username):
    
    cur.execute(f"SELECT * FROM user_table WHERE username = '{username}'")
    if cur.fetchall():
        return 1
    else:
        return 0

def on_closing(root):
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        #wn.destroy()
        root.destroy()
        quit

def main_menu(cnx, cur, root):
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
    x_coor = screen_width/2 - window_width/2
    y_coor = screen_height/2 - window_height/2
    wn.geometry("%dx%d+%d+%d" % (window_width, window_height, x_coor, y_coor))

    # Creating widgets
    menu_label = Label(frame2, text = 'Main Menu', font = ('Arial Bold', 32))
    exit_btn = Button(frame2, text = 'Exit', font = ('Arial', 14), 
                        command = lambda : [wn.destroy(), root.deiconify()])
    btn1 = Button(frame2, text = 'View / Search Players', font = ('Arial', 14),
                  command = open(cnx, cur, root))
    btn2 = Button(frame2, text = 'View / Search Teams', font = ('Arial', 14), 
                    command = lambda : print('ok') )
    btn3 = Button(frame2, text = 'View / Search All Star Teams', font = ('Arial', 14), 
                    command = lambda : print('ok') )
    btn4 = Button(frame2, text = 'View / Search Fantasy Teams', font = ('Arial', 14), 
                    command = lambda : print('ok') )
    btn5 = Button(frame2, text = 'Create a Team', font = ('Arial', 14), 
                    command = lambda : print('ok') )
        
    # Placing widgets on the screen
    menu_label.grid(row=1, column=0, columnspan=2, sticky='NEWS', pady=(20,30))
    btn1.grid(row=2, column=0, columnspan=2,sticky='NEWS')
    btn2.grid(row=3, column=0, columnspan=2, sticky='NEWS')
    btn3.grid(row=4, column=0, columnspan=2, sticky='NEWS')
    btn4.grid(row=5, column=0, columnspan=2, sticky='NEWS')
    btn5.grid(row=6, column=0, columnspan=2, sticky='NEWS')
    exit_btn.grid(row=7, column=0, columnspan=2, sticky='NEWS')

    frame2.pack(anchor = tk.CENTER)

    wn.protocol("WM_DELETE_WINDOW", lambda : on_closing(root))
    wn.mainloop()

def login(cnx, cur, root, username, password):

    if not username or not password:
        messagebox.showerror(title = 'Login Invalid', message = 'No username or password entered!')

    elif not username_exists(cur, username):
        messagebox.showerror(title = 'Login Invalid', message = 'Username does not exist!')

    else:
        cur.execute(f"SELECT * FROM user_table WHERE username = '{username}'")
        user_info = cur.fetchall()

        if user_info[0]['password'] != password:
            messagebox.showerror(title = 'Login Invalid', message = 'Incorrect password!')

        else:
            main_menu(cnx, cur, root)

    return

def open(cnx, cur, root):
    open_window(cnx, cur, root)

def register_confirm(cur, window, first_name, last_name, username, password, password_confirm):

    if not first_name or not last_name or not username or  not password or not password_confirm:
        messagebox.showwarning(title = 'Missing Information', message = 'Please Ensure All Fields Are Filled')
    elif password != password_confirm:
        messagebox.showerror(title = 'Invalid Passwords', message = 'Passwords do not match!')
    else:
        if username_exists(cur, username):
            messagebox.showerror(title = 'Invalid Username', message = 'Username already exists, please select a different one')
        else:
           cur.execute(f"CALL create_username('{username}', '{first_name}', '{last_name}', '{password}')")
           messagebox.showinfo(title = 'Success!', message = 'Account successfully created')
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
    x_coor = screen_width/2 - window_width/2
    y_coor = screen_height/2 - window_height/2
    wn.geometry("%dx%d+%d+%d" % (window_width, window_height, x_coor, y_coor))

    # Creating widgets
    create_account_label = Label(frame2, text = 'Create Your Account', font = ('Arial Bold', 20))
    first_name_label = Label(frame2, text = 'First Name', font = ('Arial', 14))
    first_name_entry = Entry(frame2)
    last_name_label = Label(frame2, text = 'Last Name', font = ('Arial', 14))
    last_name_entry = Entry(frame2)
    username_label = Label(frame2, text = 'Username', font = ('Arial', 14))
    username_entry = Entry(frame2)
    password_label = Label(frame2, text = 'Password', font = ('Arial', 14))
    password_entry = Entry(frame2, show = '*')
    password_confirm_label = Label(frame2, text = 'Confirm Password', font = ('Arial', 14))
    password_confirm_entry = Entry(frame2, show = '*')
    create_account_button = Button(frame2, text = 'Create Account', font = ('Arial', 14), 
                             command = lambda : register_confirm(cur, wn, first_name_entry.get(), last_name_entry.get(),
                                                                  username_entry.get(), password_entry.get(), password_confirm_entry.get()))
    exit_button = Button(frame2, text = 'Exit', font = ('Arial', 14), 
                         command = lambda : wn.destroy())

    # Placing widgets on the screen
    create_account_label.grid(row=1, column=0, columnspan=2, sticky='NEWS', pady=(0,10))
    first_name_label.grid(row=2, column=0, sticky = 'W')
    first_name_entry.grid(row=3, column=0, pady=(0,10))
    last_name_label.grid(row=4, column=0, sticky = 'W')
    last_name_entry.grid(row=5, column=0, pady=(0,10))
    username_label.grid(row=6, column=0, sticky = 'W')
    username_entry.grid(row=7, column=0, pady=(0,10))
    password_label.grid(row=8, column=0, sticky = 'W')
    password_entry.grid(row=9, column=0, pady=(0,10))
    password_confirm_label.grid(row=10, column=0, sticky = 'W')
    password_confirm_entry.grid(row=11, column=0, pady=(0,10))
    create_account_button.grid(row=12, column=0, sticky = 'W')
    exit_button.grid(row=12, column=0, sticky = 'E')

    frame2.pack(anchor = tk.CENTER)
    return;


def start_screen(cnx, cur, root):

    # Create Frame
    frame = tk.Frame()

    # Creating widgets
    login_label = tk.Label(frame, text = 'Login to your account', font = ('Arial Bold', 20))
    username_label = tk.Label(frame, text = 'Username', font = ('Arial', 14))
    username_entry = tk.Entry(frame)
    password_label = tk.Label(frame, text = 'Password', font = ('Arial', 14))
    password_entry = tk.Entry(frame, show = '*')
    login_button = tk.Button(frame, text = 'Login', font = ('Arial', 14),
                             command = lambda : [login(cnx, cur, root, username_entry.get(), password_entry.get())])
    register_button = tk.Button(frame, text = 'Register', font = ('Arial', 14), 
                                command = lambda : [register(cur, root), cnx.commit()])
    logo = ImageTk.PhotoImage(Image.open('nba_logo.png'))
    logo_label = tk.Label(frame, image=logo)
    logo_label.image = logo

    #Define a function to clear the Entry Widget Content
    def clear_text():
        username_entry.delete(0, END)
        password_entry.delete(0, END)

    # Placing widgets on the screen
    logo_label.grid(row=0, column=0, columnspan=2, sticky = 'NEWS')
    login_label.grid(row=1, column=0, columnspan=2, sticky='NEWS', pady=(0,10))
    username_label.grid(row=2, column=0, sticky = 'W')
    username_entry.grid(row=3, column=0, pady=(0,10))
    password_label.grid(row=4, column=0, sticky = 'W')
    password_entry.grid(row=5, column=0, pady=(0,10))
    login_button.grid(row=6, column=0, sticky = 'E')
    register_button.grid(row=6, column=0, sticky = 'W')

    frame.pack(anchor = tk.CENTER)
    root.mainloop()

    return;

def main():

    # connect to database using pymysql
    cnx = pymysql.connect(host='localhost',
                          user= 'root',
                          password= 'cs5200PROJECT!',
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
    x_coor = screen_width/2 - window_width/2
    y_coor = screen_height/2 - window_height/2
    root.geometry("%dx%d+%d+%d" % (window_width, window_height, x_coor, y_coor))
    start_screen(cnx, cur, root)

    # close db connection
    cur.close()
    cnx.close()

if __name__ == "__main__":
    main()
