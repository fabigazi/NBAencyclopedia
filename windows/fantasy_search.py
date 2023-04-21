

import customtkinter
import tkinter as tk
from tkinter import *
from tkinter import messagebox, ttk
import pandas as pd

customtkinter.set_appearance_mode("Light")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"

# join on player info and year to make team stats
def fantasy_search(cnx, cur, root, window):
    # root.withdraw()
    window.withdraw()
    # Create new window
    wn = Toplevel(root)
    frame = Frame(wn)


    # load Drop-downs
    fantasy_team_drop_down = ["Select a Team"]
    cur.execute('CALL fantasy_team_search_drop_down()')

    for row in cur.fetchall():
        fantasy_team_drop_down.append(str(row['team_name']))

    # Set window specifications and location
    window_width = 900
    window_height = 450
    screen_width = wn.winfo_screenwidth()
    screen_height = wn.winfo_screenheight()
    x_coor = screen_width / 2 - window_width / 2
    y_coor = screen_height / 2 - window_height / 2
    wn.geometry("%dx%d+%d+%d" % (window_width, window_height, x_coor, y_coor))

    # initialize variables
    is_on = {}
    df = pd.DataFrame({'player_name': pd.Series(dtype='str'),
                        'position': pd.Series(dtype='str'),
                        'team': pd.Series(dtype='str'),
                        'points_pg': pd.Series(dtype='str'),
                        'free_throw': pd.Series(dtype='str'),
                        'rebounds': pd.Series(dtype='str'),
                        'assists': pd.Series(dtype='str')})

    df = df[['player_name', 'position', 'team', 'points_pg', 'free_throw', 'rebounds', 'assists']]
    df = df.rename(
        columns={'player_name': 'Name', 'position': 'Pos', 'team': 'Team',
                 'points_pg': 'Points', 'free_throw': 'FT %', 'rebounds': 'REB', 'assists': 'Assists'})

    # tree view frame
    treeview_frame = ttk.Treeview(frame, height=18, padding=1, show="headings")
    treeview_frame.grid(row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
    treeview_frame['columns'] = list(df.columns)

    treeview_frame.column("# 1", stretch=NO, width=100)
    treeview_frame.column("# 2", stretch=NO, width=50)
    treeview_frame.column("# 3", stretch=NO, width=50)
    treeview_frame.column("# 4", stretch=NO, width=50)
    treeview_frame.column("# 5", stretch=NO, width=50)
    treeview_frame.column("# 6", stretch=NO, width=50)
    treeview_frame.column("# 7", stretch=NO, width=50)

    # Create heading columns
    for column in df.columns:
        treeview_frame.heading(column, text=column)

    # Creating widgets
    frame_filters = customtkinter.CTkFrame(frame, width=150, height=400)
    frame_filters.grid(row=0, column=0, padx=(20, 0), pady=(20, 0), sticky="nsew")
    # frame_filters.add("Player Search")
    Label = customtkinter.CTkLabel(frame_filters, text="Fantasy Team Search:")

    Label.grid(row=0, column=0, padx=20, pady=(8, 8))

    # Fantasy Team
    fantasy_team_dd = customtkinter.CTkOptionMenu(frame_filters, dynamic_resizing=False, values=fantasy_team_drop_down)

    fantasy_team_dd.grid(row=1, column=0, padx=20, pady=(10, 10))

    search_button = customtkinter.CTkButton(frame_filters, text="Search",
                                            command=lambda: [run_search(cur, fantasy_team_dd.get(), treeview_frame)])
    search_button.grid(row=5, column=0, padx=20, pady=(10, 10))

    back = customtkinter.CTkButton(frame_filters, text="Back",
                                   command=lambda: [wn.destroy(), window.deiconify()])
    back.grid(row=6, column=0, padx=20, pady=(10, 10))


    frame.pack(anchor=tk.CENTER)

    wn.protocol("WM_DELETE_WINDOW", lambda: [wn.destroy(), window.deiconify()])
    wn.mainloop()

def run_search(cur, t_name, treeview):

    input = ''
    # empty string vs null
    # if position == "Any Position":
    # year_input = "0"

    if t_name == "Any Team":
        for item in treeview.get_children():
            treeview.delete(item)

    else:
        cur.execute(f'CALL fantasy_team_roster_search("{t_name}")')

        df = pd.DataFrame({'player_name': pd.Series(dtype='str'),
                        'position': pd.Series(dtype='str'),
                        'team': pd.Series(dtype='str'),
                        'points_pg': pd.Series(dtype='str'),
                        'free_throw': pd.Series(dtype='str'),
                        'rebounds': pd.Series(dtype='str'),
                        'assists': pd.Series(dtype='str')})
        
        df = df[['player_name', 'position', 'team', 'points_pg', 'free_throw', 'rebounds', 'assists']]
        df = df.rename(
        columns={'player_name': 'Name', 'position': 'Pos', 'team': 'Team',
                 'points_pg': 'Points', 'free_throw': 'FT %', 'rebounds': 'REB', 'assists': 'Assists'})
        
        for item in treeview.get_children():
            treeview.delete(item)
        fetch = cur.fetchall()
        if fetch:
            for row in fetch:
                new_row = [row['player'],
                        row['pos'],  row['tm'],  row['pts_per_game'],
                        row['ft_percent'],  row['trb_per_game'], row['ast_per_game']]
                treeview.insert("", tk.END, values=list(new_row))

def on_closing(root):
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        # wn.destroy()
        root.destroy()
        quit