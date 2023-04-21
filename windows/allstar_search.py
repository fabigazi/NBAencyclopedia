

import customtkinter
import tkinter as tk
from tkinter import *
from tkinter import messagebox, ttk
import pandas as pd

customtkinter.set_appearance_mode("Light")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"

# join on player info and year to make team stats
def allstar_search(cnx, cur, root, window):
    # root.withdraw()
    window.withdraw()
    # Create new window
    wn = Toplevel(root)
    frame = Frame(wn)

    # load Drop-downs
    year_drop_down = ["Any Year"]
    cur.execute('CALL player_search_years_drop_down()')

    for row in cur.fetchall():
        year_drop_down.append(str(row['season']))

    team_drop_down = ["Any Team"]
    cur.execute('CALL all_star_drop_down()')

    for row in cur.fetchall():
        team_drop_down.append(str(row['team']))

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
    df = pd.DataFrame({'team': pd.Series(dtype='str'),
                       'player': pd.Series(dtype='str'),
                       'season_year': pd.Series(dtype='str')})

    df = df[['team', 'player', 'season_year']]
    df = df.rename(
        columns={'team' : 'Team', 'player': 'Player', 'season_year': 'Year'})

    # tree view frame
    treeview_frame = ttk.Treeview(frame, height=18, padding=1, show="headings")
    treeview_frame.grid(row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
    treeview_frame['columns'] = list(df.columns)

    # Create heading columns
    for column in df.columns:
        treeview_frame.heading(column, text=column)

    # Creating widgets
    frame_filters = customtkinter.CTkFrame(frame, width=150, height=400)
    frame_filters.grid(row=0, column=0, padx=(20, 0), pady=(20, 0), sticky="nsew")
    # frame_filters.add("Player Search")
    Label = customtkinter.CTkLabel(frame_filters, text="All Star Team Search:")

    Label.grid(row=0, column=0, padx=20, pady=(8, 8))

    # Year
    year_dd = customtkinter.CTkOptionMenu(frame_filters, dynamic_resizing=False, values=year_drop_down)

    year_dd.grid(row=1, column=0, padx=20, pady=(10, 10))

    # Team Name
    team_dd = customtkinter.CTkOptionMenu(frame_filters, dynamic_resizing=True, values=team_drop_down)

    team_dd.grid(row=3, column=0, padx=20, pady=(10, 10))

    search_button = customtkinter.CTkButton(frame_filters, text="Search",
                                            command=lambda: [run_search(cur, year_dd.get(),
                                                                        team_dd.get(), treeview_frame)])
    search_button.grid(row=5, column=0, padx=20, pady=(10, 10))

    back = customtkinter.CTkButton(frame_filters, text="Back",
                                   command=lambda: [wn.destroy(), window.deiconify()])
    back.grid(row=6, column=0, padx=20, pady=(10, 10))

    frame.pack(anchor=tk.CENTER)

    run_search(cur, "Any Year", "Any Team", treeview_frame)

    wn.protocol("WM_DELETE_WINDOW", lambda: [wn.destroy(), window.deiconify()])
    wn.mainloop()


def run_search(cur, year, t_name, treeview):
    # where we should run search with given inputs
    # filler = 0
    print(year)
    print(t_name)
    input = ''
    # empty string vs null
    # if position == "Any Position":
    # year_input = "0"

    if year != "Any Year":
        input += 'Y'

    if t_name != "Any Team":
        input += 'T'

    command = get_command(input, year, "", "", t_name)
    cur.execute(command)
    # cur.execute(f"CALL player_search('{p_name_input}', '{year_input}', '{position_input}', '{t_name_input}')")
    df = pd.DataFrame({'team': pd.Series(dtype='str'),
                       'player_name': pd.Series(dtype='str'),
                       'season_year': pd.Series(dtype='str')})
    
    for row in cur.fetchall():
        new_row = {'team': row['team'], 'player_name': row['player'],
                   'season_year': row['season']}
        df.loc[len(df)] = new_row

    for item in treeview.get_children():
        treeview.delete(item)

    for index, row in df.iterrows():
        treeview.insert("", tk.END, values=list(row))


def on_closing(root):
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        # wn.destroy()
        root.destroy()
        quit


def get_command(input, year, position, p_name, t_name):
    if input == '':
        return 'CALL generic_all_star_search()'
    elif input == 'Y':
        return f'CALL all_star_search_year({year})'
    elif input == 'T':
        return f'CALL all_star_search_team("{t_name}")'
    else:
        return f'CALL all_star_search_year_team({year}, "{t_name}")'
