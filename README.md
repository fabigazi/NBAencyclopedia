# NBAencyclopedia
This is the final project CS 5200 - Database Management Systems by group WebbMO’ConnellJGazianoF. Created by Maya Webb, John O'Connell, Fabian Gaziano

## Data Sets
[Kagel](https://www.kaggle.com/datasets/sumitrodatta/nba-aba-baa-stats)
* all_star_selections
* end_of_season_teams
* player_career_info
* player_final
* player_season_info
* team_abbrev
* user_table

## Dependencies:

* Django	4.2	4.2
* Pillow 9.5.0	
* PyMySQL	1.0.2	
* asgiref	3.6.0	
* cffi	1.15.1
* cryptography	40.0.2	
* customtkinter	5.1.2	
* darkdetect	0.8.0
* image	1.5.33	
* numpy	1.24.2
* pandas	2.0.0
* pip	22.3.1
* pycparser	2.21
* python-dateutil	2.8.2
* pytz	2023.3
* setuptools	65.5.1
* six	1.16.0
* sqlparse	0.4.3
* tzdata	2023.3
* wheel	0.38.4

### Run the following command in a terminal where the project is located:

pip install Django, Pillow, PyMySQL, asgiref, cffi, cryptography, customtkinter, darkdetect, image, numpy, pandas, pip, pycparser, python-dateutil, pytz, setuptools, six, sqlparse, tzdata, wheel


## Run Instructions:

    1. put the project in the desired location
    2. open terminal to the location determined in step one
    3. run the pip install dependencies as given above.
    4. run the command: python3 nba_encyclopedia.py

## UI overview:

### Login:

The user is presented with a login screen where they can either input their existing username and
password and select login taking them to the Main Window, or select register to take them to a user 
registration window.

### Create Account:

The user can input their relevant information and select Register or select Exit. in both cases the user
is brought back to the Login Window.

### Main Menu:

The user can select any of the following options and will be brought to their respective windows.
* View / Search Players
* View / Search Teams
* View / Search All Star Teams
* View / Search Fantasy Teams
* Create Team

Exit will bring the user back to the Login window.

### View / Search Players:
The following are a list of inputs the user can use to look up specific values in the database. The 
drop-downs are populated from the database. Once the user is satisfied with any combination of selected
fields the user can select the search button to query the DB.

* Year
* Position
* Team
* Player Name

Back button will bring the user back to the main menu

### View / Search Teams
### View / Search All Star Teams
### View / Search Fantasy Teams
### Create Team