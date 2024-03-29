# NBAencyclopedia
This is the final project CS 5200 - Database Management Systems by group WebbMO’ConnellJGazianoF. Created by Maya Webb, John O'Connell, Fabian Gaziano

## Project File Structure

* data - csv files used to clean data
* images - full images of ERD and reverse engineer of DB
* sql - folder containing all sql files 
  * nba_app_DUMP_final.sql is the master sql file containing all tables, stored procedures, and triggers
* windows - contain the 7 different windows we implemented
* data cleaning files - are some methods we used to clean the data sets
* nba_encyclopedia.py - the main python file for the project containing the main menu and register

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

    1. In my sql workbench exicute the file nba_app_DUMP_final.sql
    2. put the project in the desired location
    3. open terminal to the location determined in step one
    4. run the pip install dependencies as given above.
    5. run the command: python3 nba_encyclopedia.py
