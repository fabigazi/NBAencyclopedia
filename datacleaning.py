import pandas as pd

df = pd.read_csv('stats/Player_Career_Info.csv')

df = pd.read_csv('stats/Player_Season_Info.csv')

count = 0
for index, name in enumerate(df['player']):
    try:
        name = name.encode('ascii').decode()
    except UnicodeEncodeError:
        df = df.drop([index])

print (df.shape)
df.to_csv('stats/player_season_info_final.csv', index=False)

df = pd.read_csv('stats/Player_Final.csv')

count = 0
for index, name in enumerate(df['player']):
    try:
        name = name.encode('ascii').decode()
    except UnicodeEncodeError:
        df = df.drop([index])

print (df.shape)

df.to_csv('stats/player_final_final.csv', index=False)


