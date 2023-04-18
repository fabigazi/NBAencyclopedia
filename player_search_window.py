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
    #root.withdraw()
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
    tab_view_filters = customtkinter.CTkTabview(frame3, width=150, height=400)
    tab_view_filters.grid(row=0, column=0, padx=(20, 0), pady=(20, 0), sticky="nsew")
    tab_view_filters.add("Player Search")

    # TODO: fill with data from DB
    year_dd = customtkinter.CTkOptionMenu(tab_view_filters.tab("Player Search"),
                                          dynamic_resizing=True,
                                          values=["Any Year", "2023", "2022", "2021"])

    year_dd.grid(row=0, column=0, padx=20, pady=(10, 10))

    # TODO: fill with data from DB
    position_dd = customtkinter.CTkOptionMenu(tab_view_filters.tab("Player Search"),
                                              dynamic_resizing=True,
                                              values=["Any Position", "SG", "SF", "PF"])

    position_dd.grid(row=1, column=0, padx=20, pady=(10, 10))

    player_name_entry = customtkinter.CTkEntry(tab_view_filters.tab("Player Search"),
                                               placeholder_text="Player Name")
    player_name_entry.grid(row=2, column=0, padx=20, pady=(10, 10))

    team_name_entry = customtkinter.CTkEntry(tab_view_filters.tab("Player Search"),
                                             placeholder_text="Team Name")
    team_name_entry.grid(row=3, column=0, padx=20, pady=(10, 10))

    search_button = customtkinter.CTkButton(tab_view_filters.tab("Player Search"), text="Search",
                                            command=lambda: [run_search(year_dd, position_dd, player_name_entry,
                                                                        team_name_entry)])
    search_button.grid(row=4, column=0, padx=20, pady=(10, 10))

    back = customtkinter.CTkButton(tab_view_filters.tab("Player Search"), text="Back",
                                            command=lambda: [wn.destroy(), window.deiconify()])
    back.grid(row=5, column=0, padx=20, pady=(10, 10))

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


def run_search(year, position, p_name, t_name):
    # where we should run search with given inputs
    filler = 0
    print(year.get())
    print(position.get())
    print(p_name)
    print(t_name)

def on_closing(root):
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        #wn.destroy()
        root.destroy()
        quit
