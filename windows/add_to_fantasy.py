import customtkinter
import tkinter as tk
from tkinter import *
from tkinter import messagebox, ttk
import pandas as pd

from windows.populate_dds import *

# from windows.create_fantasy import user_fantasy_search

customtkinter.set_appearance_mode("Light")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"


def open_add_to_fantasy(username, team_name, cnx, cur, root, window, old_treeview):
    # root.withdraw()
    window.withdraw()
    # Create new window
    wn = Toplevel(root)
    frame3 = Frame(wn)

    # load Drop-downs
    year_drop_down = load_season_dd(cur)

    position_drop_down = load_position_dd(cur)

    team_drop_down = load_team_dd(cur)

    # Set window specifications and location
    window_width = 1300
    window_height = 450
    screen_width = wn.winfo_screenwidth()
    screen_height = wn.winfo_screenheight()
    x_coor = screen_width / 2 - window_width / 2
    y_coor = screen_height / 2 - window_height / 2
    wn.geometry("%dx%d+%d+%d" % (window_width, window_height, x_coor, y_coor))

    # initialize variables
    df_search = pd.DataFrame({'player_name': pd.Series(dtype='str'),
                              'season_year': pd.Series(dtype='str'),
                              'position': pd.Series(dtype='str'),
                              'team': pd.Series(dtype='str')})

    df_search = df_search[['player_name', 'season_year', 'position', 'team']]
    df_search = df_search.rename(columns={'player_name': 'Name', 'season_year': 'Year',
                                          'position': 'Position', 'team': 'Team'})

    df_team = pd.DataFrame({'player': pd.Series(dtype='str'),
                            'position': pd.Series(dtype='str'),
                            'team': pd.Series(dtype='str')})

    df_team = df_team[['player', 'position', 'team']]
    df_team = df_team.rename(
        columns={'player': 'Name', 'position': 'Position', 'team': 'Team'})

    # tree view frame
    treeview_search = ttk.Treeview(frame3, height=18, padding=1, show="headings")
    treeview_search.grid(row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
    treeview_search['columns'] = list(df_search.columns)

    treeview_search.column("# 1", stretch=NO, width=100)
    treeview_search.column("# 2", stretch=NO, width=100)
    treeview_search.column("# 3", stretch=NO, width=100)
    treeview_search.column("# 4", stretch=NO, width=100)

    treeview_fantasy = ttk.Treeview(frame3, height=18, padding=1, show="headings")
    treeview_fantasy.grid(row=0, column=3, padx=(20, 0), pady=(20, 0), sticky="nsew")
    treeview_fantasy['columns'] = list(df_team.columns)

    treeview_fantasy.column("# 1", stretch=NO, width=100)
    treeview_fantasy.column("# 2", stretch=NO, width=100)
    treeview_fantasy.column("# 3", stretch=NO, width=100)

    # Create heading columns
    for column in df_search.columns:
        treeview_search.heading(column, text=column)

    for column in df_team.columns:
        treeview_fantasy.heading(column, text=column)

    # Createing widgets
    frame_filters1 = customtkinter.CTkFrame(frame3, width=150, height=400)
    frame_filters1.grid(row=0, column=0, padx=(20, 0), pady=(20, 0), sticky="nsew")
    # frame_filters.add("Player Search")
    label = customtkinter.CTkLabel(frame_filters1, text="Search Players:")

    label.grid(row=0, column=0, padx=20, pady=(8, 8))

    # Position
    position_dd = customtkinter.CTkOptionMenu(frame_filters1, dynamic_resizing=True, values=position_drop_down)

    position_dd.grid(row=2, column=0, padx=20, pady=(10, 10))

    # Team Name
    team_name_entry = customtkinter.CTkOptionMenu(frame_filters1, dynamic_resizing=True, values=team_drop_down)

    team_name_entry.grid(row=3, column=0, padx=20, pady=(10, 10))

    # Player Name
    player_name_entry = customtkinter.CTkEntry(frame_filters1,
                                               placeholder_text="Player Name")
    player_name_entry.grid(row=4, column=0, padx=20, pady=(10, 10))

    search_button = customtkinter.CTkButton(frame_filters1, text="Search",
                                            command=lambda: [run_search(cur, "2023", position_dd.get(),
                                                                        player_name_entry.get(),
                                                                        team_name_entry.get(), treeview_search)])
    search_button.grid(row=5, column=0, padx=20, pady=(10, 10))

    back = customtkinter.CTkButton(frame_filters1, text="Back",
                                   command=lambda: [wn.destroy(), window.deiconify()])
    back.grid(row=6, column=0, padx=20, pady=(10, 10))

    # Createing widgets
    frame_filters2 = customtkinter.CTkFrame(frame3, width=150, height=400)
    frame_filters2.grid(row=0, column=2, padx=(20, 0), pady=(20, 0), sticky="nsew")
    # frame_filters.add("Player Search")
    label2 = customtkinter.CTkLabel(frame_filters2, text="Edit Fantasy Team:")

    label2.grid(row=0, column=0, padx=20, pady=(0, 0))

    label3 = customtkinter.CTkLabel(frame_filters2, text=team_name)

    label3.grid(row=1, column=0, padx=20, pady=(0, 0))

    add = customtkinter.CTkButton(frame_filters2, text="Add Player >",
                                  command=lambda: [add_player(cur, username, team_name, treeview_search, old_treeview)])
    add.grid(row=2, column=0, padx=20, pady=(0, 10))

    delete = customtkinter.CTkButton(frame_filters2, text="Delete Player",
                                     command=lambda: [delete_player(cur, username,team_name, treeview_fantasy, old_treeview),
                                                      cnx.commit()])
    delete.grid(row=3, column=0, padx=20, pady=(10, 10))

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


# updates the user team table count
def user_fantasy_add_update(cur, username, old_treeview):
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

    for item in old_treeview.get_children():
        old_treeview.delete(item)

    if not df_trimmed.empty:
        for index, row in df_trimmed.iterrows():
            old_treeview.insert("", tk.END, values=list(row))


# deletes a player from the team
def delete_player(cur, username, team_name, treeview, old_treeview):
    try:
        line_selected = treeview.item(treeview.focus())
        team_name = line_selected['values'][0]

        cur.execute(f"CALL fantasy_player_delete('{username}','{team_name}')")
        user_team_select(cur, username, team_name, treeview)
        user_fantasy_add_update(cur, username, old_treeview)
    except:
        messagebox.showerror(title='No Team Selected', message='Please select a team')


def add_player(cur, username, team_name, treeview, old_treeview):
    line_selected = treeview.item(treeview.focus())
    player = line_selected['values'][0]  # player name

    cur.execute(f"CALL player_to_player_id('{player}')")

    test = cur.fetchall()[0]
    test = test['player_id']

    cur.execute(f"CALL fantasy_players_add('{username}','{team_name}', '{test}')")
    user_team_select(cur, username, team_name, treeview)
    user_fantasy_add_update(cur, username, old_treeview)
    try:
        test = 10
    except:
        messagebox.showerror(title='No Player Sel', message='Please select a player')


# updates the players treeview table from db
def user_team_select(cur, username, team_name, treeview):
    cur.execute(f"CALL fantasy_player_search('{username}', '{team_name}')")
    df = pd.DataFrame({'players': pd.Series(dtype='str'),
                       'position': pd.Series(dtype='str'), 'team': pd.Series(dtype='str')})

    df_trimmed = pd.DataFrame({'players': pd.Series(dtype='str'),
                               'position': pd.Series(dtype='str'), 'team': pd.Series(dtype='str')})

    for row in cur.fetchall():
        new_row = {'players': row['player'], 'position': row['pos'], 'team': row['tm']}
        df.loc[len(df)] = new_row

    if not df.empty:
        df_trimmed = df[["players", "position", "team"]]

    for item in treeview.get_children():
        treeview.delete(item)

    if not df_trimmed.empty:
        for index, row in df_trimmed.iterrows():
            treeview.insert("", tk.END, values=list(row))
