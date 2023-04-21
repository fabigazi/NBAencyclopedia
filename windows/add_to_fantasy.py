

import customtkinter
import tkinter as tk
from tkinter import *
from tkinter import messagebox, ttk
import pandas as pd

# from windows.create_fantasy import user_fantasy_search

customtkinter.set_appearance_mode("Light")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"


def open_add_to_fantasy(username, team_name, cnx, cur, root, window, treeview):
    # root.withdraw()
    window.withdraw()
    # Create new window
    wn = Toplevel(root)
    frame3 = Frame(wn)

    # load Drop-downs
    year_drop_down = ["Any Year"]
    cur.execute('CALL player_search_years_drop_down()')

    for row in cur.fetchall():
        year_drop_down.append(str(row['season']))

    position_drop_down = ["Any Position"]
    cur.execute('CALL player_search_position_drop_down()')

    for row in cur.fetchall():
        position_drop_down.append(str(row['pos']))

    team_drop_down = ["Any Team"]
    cur.execute('CALL player_search_team_drop_down()')

    for row in cur.fetchall():
        team_drop_down.append(str(row['abbreviation']))

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
                       'season_year': pd.Series(dtype='str')})

    df = df[['team', 'season_year']]
    df = df.rename(
        columns={'team': 'Team', 'season_year': 'Year'})

    # tree view frame
    treeview_search = ttk.Treeview(frame3, height=18, padding=1, show="headings")
    treeview_search.grid(row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
    treeview_search['columns'] = list(df.columns)

    treeview_fantasy = ttk.Treeview(frame3, height=18, padding=1, show="headings")
    treeview_fantasy.grid(row=0, column=2, padx=(20, 0), pady=(20, 0), sticky="nsew")
    treeview_fantasy['columns'] = list(df.columns)

    # Create heading columns
    for column in df.columns:
        treeview_search.heading(column, text=column)

    # Createing widgets
    frame_filters = customtkinter.CTkFrame(frame3, width=150, height=400)
    frame_filters.grid(row=0, column=0, padx=(20, 0), pady=(20, 0), sticky="nsew")
    # frame_filters.add("Player Search")
    Label = customtkinter.CTkLabel(frame_filters, text="Create Fantasy Team:")

    Label.grid(row=0, column=0, padx=20, pady=(8, 8))

    # Year
    year_dd = customtkinter.CTkOptionMenu(frame_filters, dynamic_resizing=False, values=year_drop_down)

    year_dd.grid(row=1, column=0, padx=20, pady=(0, 10))

    # Position
    position_dd = customtkinter.CTkOptionMenu(frame_filters, dynamic_resizing=True, values=position_drop_down)

    position_dd.grid(row=2, column=0, padx=20, pady=(10, 10))

    # Team Name
    team_name_entry = customtkinter.CTkOptionMenu(frame_filters, dynamic_resizing=True, values=team_drop_down)

    team_name_entry.grid(row=3, column=0, padx=20, pady=(10, 10))

    # Player Name
    player_name_entry = customtkinter.CTkEntry(frame_filters,
                                               placeholder_text="Player Name")
    player_name_entry.grid(row=4, column=0, padx=20, pady=(10, 10))

    search_button = customtkinter.CTkButton(frame_filters, text="Search",
                                            command=lambda: [run_search(cur, year_dd.get(), position_dd.get(),
                                                                        player_name_entry.get(),
                                                                        team_name_entry.get(), treeview_search)])
    search_button.grid(row=5, column=0, padx=20, pady=(10, 10))

    #add = customtkinter.CTkButton(frame_filters, text="Add",
                             #      command=lambda: [wn.destroy(), window.deiconify(),
                                             #       user_fantasy_search(cur, username, treeview)])
    #add.grid(row=6, column=0, padx=20, pady=(10, 10))

    back = customtkinter.CTkButton(frame_filters, text="Back",
                                   command=lambda: [wn.destroy(), window.deiconify()])
    back.grid(row=7, column=0, padx=20, pady=(10, 10))

    frame3.pack(anchor=tk.CENTER)

    wn.protocol("WM_DELETE_WINDOW", lambda: [wn.destroy(), window.deiconify()])
    wn.mainloop()


def run_search(cur, year, position, p_name, t_name, treeview):
    # where we should run search with given inputs
    # filler = 0
    print(year)
    print(position)
    print(p_name)
    print(t_name)
    input = ''
    # empty string vs null
    # if position == "Any Position":
    # year_input = "0"

    if year != "Any Year":
        input += 'Y'

    if position != "Any Position":
        input += 'P'

    if p_name != "":
        input += 'N'

    if t_name != "Any Team":
        input += 'T'

    command = get_command(input, year, position, p_name, t_name)
    cur.execute(command)
    # cur.execute(f"CALL player_search('{p_name_input}', '{year_input}', '{position_input}', '{t_name_input}')")
    df = pd.DataFrame({'player_name': pd.Series(dtype='str'),
                       'season_year': pd.Series(dtype='str'),
                       'position': pd.Series(dtype='str'),
                       'team': pd.Series(dtype='str')})
    for row in cur.fetchall():
        new_row = {'player_name': row['player'], 'season_year': row['season'],
                   'position': row['pos'], 'team': row['tm']}
        df.loc[len(df)] = new_row

    if not df.empty:
        df_trimmed = df[["player_name", "season_year", "position", "team"]]

    for item in treeview.get_children():
        treeview.delete(item)

    for index, row in df_trimmed.iterrows():
        treeview.insert("", tk.END, values=list(row))


def on_closing(root):
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        # wn.destroy()
        root.destroy()
        quit


def get_command(input, year, position, p_name, t_name):
    if input == '':
        return 'CALL generic_player_search()'
    elif input == 'Y':
        return f'CALL player_search_year({year})'
    elif input == 'P':
        return f'CALL player_search_pos("{position}")'
    elif input == 'N':
        return f'CALL player_search_name("{p_name}")'
    elif input == 'T':
        return f'CALL player_search_team("{t_name}")'
    elif input == 'YP':
        return f'CALL player_search_year_pos({year}, "{position}")'
    elif input == 'YN':
        return f'CALL player_search_year_name({year}, "{p_name}")'
    elif input == 'YT':
        return f'CALL player_search_year_team({year}, "{t_name}")'
    elif input == 'PN':
        return f'CALL player_search_pos_name("{position}", "{p_name}")'
    elif input == 'PT':
        return f'CALL player_search_pos_team("{position}", "{t_name}")'
    elif input == 'NT':
        return f'CALL player_search_name_team("{p_name}", "{t_name}")'
    elif input == 'YPN':
        return f'CALL player_search_year_pos_name({year}, "{position}", "{p_name}")'
    elif input == 'YPT':
        return f'CALL player_search_year_pos_team({year}, "{position}", "{t_name}")'
    elif input == 'PNT':
        return f'CALL player_search_pos_name_team("{position}", "{p_name}", "{t_name}")'
    else:
        return f'CALL player_search_all({year}, "{position}", "{p_name}", "{t_name}")'
