import math

import customtkinter
import pymysql
import tkinter as tk
from tkinter import *
from tkinter import messagebox, ttk
import pandas as pd
from PIL import Image, ImageTk

customtkinter.set_appearance_mode("Light")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"


def open_window(cnx, cur, root, window):
    # root.withdraw()
    window.withdraw()
    # Create new window
    wn = Toplevel(root)
    frame3 = Frame(wn)

    # Set window specifications and location
    window_width = 1100
    window_height = 450
    screen_width = wn.winfo_screenwidth()
    screen_height = wn.winfo_screenheight()
    x_coor = screen_width / 2 - window_width / 2
    y_coor = screen_height / 2 - window_height / 2
    wn.geometry("%dx%d+%d+%d" % (window_width, window_height, x_coor, y_coor))

    # initialize variables
    is_on = {}
    df_sorted = df = pd.DataFrame({'player_name': pd.Series(dtype='str'),
                                   'season_year': pd.Series(dtype='str'),
                                   'position': pd.Series(dtype='str'),
                                   'team': pd.Series(dtype='str')})

    df_sorted = df_sorted[['player_name', 'season_year', 'position', 'team']]
    df_sorted = df_sorted.rename(
        columns={'player_name': 'Name', 'season_year': 'Year', 'position': 'Position', 'team': 'Team'})

    # Createing widgets
    frame_filters = customtkinter.CTkFrame(frame3, width=150, height=400)
    frame_filters.grid(row=0, column=0, padx=(20, 0), pady=(20, 0), sticky="nsew")
    #frame_filters.add("Player Search")
    Label = customtkinter.CTkLabel(frame_filters, text="Player Search:")

    Label.grid(row=0, column=0, padx=20, pady=(8, 8))

    # TODO: fill with data from DB
    year_dd = customtkinter.CTkOptionMenu(frame_filters,
                                          dynamic_resizing=True,
                                          values=["Any Year", "2023", "2022", "2021"])

    year_dd.grid(row=1, column=0, padx=20, pady=(10, 10))

    # TODO: fill with data from DB
    position_dd = customtkinter.CTkOptionMenu(frame_filters,
                                              dynamic_resizing=True,
                                              values=["Any Position", "SG", "SF", "PF"])

    position_dd.grid(row=2, column=0, padx=20, pady=(10, 10))

    player_name_entry = customtkinter.CTkEntry(frame_filters,
                                               placeholder_text="Player Name")
    player_name_entry.grid(row=3, column=0, padx=20, pady=(10, 10))

    team_name_entry = customtkinter.CTkEntry(frame_filters,
                                             placeholder_text="Team Name")
    team_name_entry.grid(row=4, column=0, padx=20, pady=(10, 10))

    search_button = customtkinter.CTkButton(frame_filters, text="Search",
                                            command=lambda: [run_search(cur, year_dd.get(), position_dd.get(),
                                                                        player_name_entry.get(),
                                                                        team_name_entry.get())])
    search_button.grid(row=5, column=0, padx=20, pady=(10, 10))

    back = customtkinter.CTkButton(frame_filters, text="Back",
                                   command=lambda: [wn.destroy(), window.deiconify()])
    back.grid(row=6, column=0, padx=20, pady=(10, 10))

    # tree view frame
    treeview_frame = ttk.Treeview(frame3, height=18, padding=1, show="headings")
    treeview_frame.grid(row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
    treeview_frame['columns'] = list(df_sorted.columns)

    # Create heading columns
    for column in df_sorted.columns:
        treeview_frame.heading(column, text=column)

    frame3.pack(anchor=tk.CENTER)

    wn.protocol("WM_DELETE_WINDOW", lambda: [wn.destroy(), window.deiconify()])
    wn.mainloop()


def run_search(cur, year, position, p_name, t_name):
    # where we should run search with given inputs
    filler = 0
    print(year)
    print(position)
    print(p_name)
    print(t_name)

    year_input = year
    position_input = position
    p_name_input = p_name
    t_name_input = t_name

    # empty string vs null
    if year == "Any Year":
        year_input = "NULL"

    if position == "Any Position":
        position_input = "NULL"

    if p_name == "":
        p_name_input = "NULL"

    if t_name == "":
        t_name_input = "NULL"

    cur.execute(f"CALL player_search('{year_input}', '{position_input}', '{p_name_input}', '{t_name_input}')")


def on_closing(root):
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        # wn.destroy()
        root.destroy()
        quit
