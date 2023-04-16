import os
import pandas as pd
import customtkinter
import math
import numpy as np
import customtkinter

if __name__ == '__main__':
    current_directory = os.getcwd()

    df = pd.read_csv(current_directory + "\\data\\Player Career Info.csv")

    output = pd.DataFrame(columns=['Name', 'Mathematics', 'Science'])

    for index, row in df.iterrows():
        # Define the new row to be added
        new_row = {'Name': row['player'], 'Mathematics': 96, 'Science': 90}

        # Use the loc method to add the new row to the DataFrame
        output.loc[len(output)] = new_row

    test = 10
    output.to_csv('output', sep='\t', encoding='utf-8')