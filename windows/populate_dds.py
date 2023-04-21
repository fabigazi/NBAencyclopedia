"""
Populate_dds - a central py file to load all the drop-downs that
are repeated across the project
"""


def load_season_dd(cur):
    year_drop_down = ["Any Year"]
    cur.execute('CALL player_search_years_drop_down()')

    for row in cur.fetchall():
        year_drop_down.append(str(row['season']))

    return year_drop_down


def load_position_dd(cur):
    position_drop_down = ["Any Position"]
    cur.execute('CALL player_search_position_drop_down()')

    for row in cur.fetchall():
        position_drop_down.append(str(row['pos']))

    return position_drop_down


def load_position_dd_2(cur):
    position_drop_down = ["Any Position"]
    cur.execute('CALL player_search_position_drop_down_two(2023)')

    for row in cur.fetchall():
        position_drop_down.append(str(row['pos']))

    return position_drop_down


def load_team_dd(cur):
    team_drop_down = ["Any Team"]
    cur.execute('CALL player_search_team_drop_down()')

    for row in cur.fetchall():
        team_drop_down.append(str(row['abbreviation']))

    return team_drop_down
