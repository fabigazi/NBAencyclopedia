import tkinter as tk
from PIL import Image, ImageTk

root = tk.Tk()
root.title('NBA Application')

window_width = 500
window_height = 400
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_coor = screen_width/2 - window_width/2
y_coor = screen_height/2 - window_height/2

root.geometry("%dx%d+%d+%d" % (window_width, window_height, x_coor, y_coor))

def login():
    return;
    # create login functionality

def register():
    return;
    # create register functionality

# Create Frame
frame = tk.Frame()


# Creating widgets
login_label = tk.Label(frame, text = 'Login to your account', font = ('Arial Bold', 20))
username_label = tk.Label(frame, text = 'Username', font = ('Arial', 14))
username_entry = tk.Entry(frame)
password_label = tk.Label(frame, text = 'Password', font = ('Arial', 14))
password_entry = tk.Entry(frame, show = '*')
login_button = tk.Button(frame, text = 'Login', font = ('Arial', 14), command = login)
register_button = tk.Button(frame, text = 'Register', font = ('Arial', 14), command = register)
#logo = Image.open('nba_logo.png')
#logo = logo.resize((163, 96))
logo = ImageTk.PhotoImage(Image.open('nba_logo.png'))
#logo = ImageTk.PhotoImage(logo)
logo_label = tk.Label(frame, image=logo)
logo_label.image = logo

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
