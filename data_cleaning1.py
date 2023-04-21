import os
import pandas as pd
import customtkinter
import math
import numpy as np
import customtkinter

if __name__ == '__main__':
    current_directory = os.getcwd()

    df = pd.read_csv(current_directory + "\\data\\Player Career Info.csv")
    # player_id, player, birth_year, hof, num_seasons, first_seas, last_seas,
    output = pd.DataFrame(columns=['player_id', 'player', 'hof', 'num_seasons',
                                   'first_seas', 'last_seas'])

    for index, row in df.iterrows():
        # Define the new row to be added
        try:
            new_row = {'player_id': row['player_id'], 'player': row['player'],
                   'hof': row['hof'], 'num_seasons': row['num_seasons'], 'first_seas': row['first_seas'],
                   'last_seas': row['last_seas']}
        except:
            print(row)

        # Use the loc method to add the new row to the DataFrame
        output.loc[len(output)] = new_row

    test = 10
    # output.to_csv('', sep=',', encoding='utf-8')