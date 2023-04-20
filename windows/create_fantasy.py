import customtkinter
import tkinter as tk
from tkinter import *
from tkinter import messagebox, ttk
import pandas as pd

from windows.populate_dds import *

customtkinter.set_appearance_mode("Light")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"


def open_create_fantasy(username, cur, root, window):
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
    df = pd.DataFrame({'team': pd.Series(dtype='str'),
                       'players': pd.Series(dtype='str')})

    df = df[['team', 'players']]
    df = df.rename(
        columns={'team': 'Team', 'players': 'Players'})

    # tree view frame
    treeview_fantasy = ttk.Treeview(frame3, height=18, padding=1, show="headings")
    treeview_fantasy.grid(row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
    treeview_fantasy['columns'] = list(df.columns)

    # Create heading columns
    for column in df.columns:
        treeview_fantasy.heading(column, text=column)

    # Createing widgets
    frame_filters = customtkinter.CTkFrame(frame3, width=150, height=400)
    frame_filters.grid(row=0, column=0, padx=(20, 0), pady=(20, 0), sticky="nsew")
    # frame_filters.add("Player Search")
    Label = customtkinter.CTkLabel(frame_filters, text="Create/Select Fantasy Team:")

    Label.grid(row=0, column=0, padx=20, pady=(8, 8))

    # Team Name
    team_name_entry = customtkinter.CTkEntry(frame_filters,
                                             placeholder_text="Team Name")
    team_name_entry.grid(row=4, column=0, padx=20, pady=(10, 10))

    add = customtkinter.CTkButton(frame_filters, text="Add New Team",
                                  command=lambda: [add_team(cur, username, team_name_entry.get(), treeview_fantasy)])
    add.grid(row=6, column=0, padx=20, pady=(10, 10))

    delete = customtkinter.CTkButton(frame_filters, text="Delete Team",
                                     command=lambda: [delete_team(cur, username, treeview_fantasy)])
    delete.grid(row=7, column=0, padx=20, pady=(10, 10))

    back = customtkinter.CTkButton(frame_filters, text="Back",
                                   command=lambda: [wn.destroy(), window.deiconify()])
    back.grid(row=8, column=0, padx=20, pady=(10, 10))

    user_fantasy_search(cur, username, treeview_fantasy)

    frame3.pack(anchor=tk.CENTER)

    wn.protocol("WM_DELETE_WINDOW", lambda: [wn.destroy(), window.deiconify()])
    wn.mainloop()


def add_team(cur, username, team_name, treeview):
    # should I check if it exists first or run and then handle error
    cur.execute(f"CALL fantasy_team_add('{username}','{team_name}')")
    user_fantasy_search(cur, username, treeview)


def delete_team(cur, username, treeview):
    line_selected = treeview.item(treeview.focus())
    team_name = line_selected['values'][0]

    cur.execute(f"CALL fantasy_team_delete('{username}','{team_name}')")
    user_fantasy_search(cur, username, treeview)


def user_fantasy_search(cur, username, treeview):
    cur.execute(f"CALL fantasy_team_search('{username}')")
    # cur.execute(f"CALL player_search('{p_name_input}', '{year_input}', '{position_input}', '{t_name_input}')")
    df = pd.DataFrame({'team': pd.Series(dtype='str'),
                       'players': pd.Series(dtype='str')})
    
    df_trimmed = pd.DataFrame({'team': pd.Series(dtype='str'),
                               'players': pd.Series(dtype='str')})
    for row in cur.fetchall():
        new_row = {'team': row['team_name'], 'players': row['player_count']}
        df.loc[len(df)] = new_row

    if not df.empty:
        df_trimmed = df[["team", "players"]]

    for item in treeview.get_children():
        treeview.delete(item)

    if not df_trimmed.empty:
        for index, row in df_trimmed.iterrows():
            treeview.insert("", tk.END, values=list(row))


def on_closing(root):
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        # wn.destroy()
        root.destroy()
        quit
