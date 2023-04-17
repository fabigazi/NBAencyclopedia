import math

import numpy as np
import customtkinter
import tkinter as tk
from tkinter import ttk
import pandas as pd

import os

customtkinter.set_appearance_mode("Light")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("green")  # Themes: "blue" (standard), "green", "dark-blue"

latitude = 45.316094085851695
longitude = -69.3804148103108

df_sorted = df = pd.DataFrame({'name': pd.Series(dtype='str'),
                               'area_name': pd.Series(dtype='str'),
                               'city_name': pd.Series(dtype='str'),
                               'state_name': pd.Series(dtype='str')})

df_sorted = df_sorted[['name', 'area_name', 'city_name', 'state_name']]
df_sorted = df_sorted.rename(
    columns={'name': 'Trail Name', 'area_name': 'Area', 'city_name': 'City', 'state_name': 'State'})
features = []
activity = []

user_preferences = {}


class Window(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.is_on = {}

        # configure window
        self.title("Trail Recommender")
        self.geometry(f"{1145}x{675}")

        # when defining the row and col of the over arching grid

        # create tabview
        self.tab_view_filters = customtkinter.CTkTabview(self, width=1110, height=230)
        self.tab_view_filters.grid(row=0, column=0, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.tab_view_filters.add("Trail Preferences")
        self.tab_view_filters.add("Features")
        self.tab_view_filters.add("Activities")
        self.tab_view_filters.tab("Trail Preferences").grid_columnconfigure(3, weight=1)  # configure grid of
        # individual tabs
        self.tab_view_filters.tab("Features").grid_columnconfigure(0, weight=1)

        # self.tabview.tab("tabX") assigns the obect to the given tabX tab
        self.popularity_entry = customtkinter.CTkEntry(self.tab_view_filters.tab("Trail Preferences"),
                                                       placeholder_text="Popularity 0-85")
        self.popularity_entry.grid(row=0, column=0, padx=20, pady=(10, 10))
        # TODO: mi -> ft
        self.length_entry = customtkinter.CTkEntry(self.tab_view_filters.tab("Trail Preferences"),
                                                   placeholder_text="length in ft")
        self.length_entry.grid(row=0, column=1, padx=20, pady=(10, 10))

        self.elevation_entry = customtkinter.CTkEntry(self.tab_view_filters.tab("Trail Preferences"),
                                                      placeholder_text="elevation in ft")
        self.elevation_entry.grid(row=0, column=2, padx=20, pady=(10, 10))

        # self.slider_1 = customtkinter.CTkSlider(self.tab_view_filters.tab("Trail Preferences"), from_=0, to=1,
        #                                       number_of_steps=4)
        # self.slider_1.grid(row=0, column=3, padx=(20, 10), pady=(10, 10), sticky="ew")

        self.difficulty = customtkinter.CTkOptionMenu(self.tab_view_filters.tab("Trail Preferences"),
                                                      dynamic_resizing=True,
                                                      values=["Any Difficulty", "1", "2", "3", "4", "5"])

        self.difficulty.grid(row=0, column=3, padx=20, pady=(10, 10))

        self.radius = customtkinter.CTkEntry(self.tab_view_filters.tab("Trail Preferences"),
                                             placeholder_text="Search Radius in mi")
        self.radius.grid(row=0, column=4, padx=20, pady=(10, 10))

        self.dog_preference = customtkinter.CTkOptionMenu(self.tab_view_filters.tab("Trail Preferences"),
                                                          dynamic_resizing=True,
                                                          values=["No Dog Preferences", "dogs", "dogs-leash",
                                                                  "dogs-no"])

        self.dog_preference.grid(row=0, column=5, padx=20, pady=(10, 10))

        self.lat_long = customtkinter.CTkButton(self.tab_view_filters.tab("Trail Preferences"), text="Zip Code",
                                                command=self.input_latitude_and_longitude)
        self.lat_long.grid(row=4, column=4, padx=20, pady=(10, 10))

        self.search_button = customtkinter.CTkButton(self.tab_view_filters.tab("Trail Preferences"), text="Search",
                                                     command=self.run_search)
        self.search_button.grid(row=4, column=5, padx=20, pady=(10, 10))

        self.search_button1 = customtkinter.CTkButton(self.tab_view_filters.tab("Features"), text="Search",
                                                      command=self.run_search)
        self.search_button1.grid(row=3, column=7, padx=20, pady=(10, 10))

        self.search_button2 = customtkinter.CTkButton(self.tab_view_filters.tab("Activities"), text="Search",
                                                      command=self.run_search)
        self.search_button2.grid(row=3, column=6, padx=20, pady=(10, 10))

        # added to the activity tab
        self.activity_switches = []

        global activity
        activity = ["cross-country-skiing", "mountain-biking", "trail-running", "snowboarding",
                    "road-biking", "fishing", "walking",
                    "whitewater-kayaking", "scenic-driving", "ice-climbing", "backpacking",
                    "canoeing", "birding", "hiking",
                    "horseback-riding", "paddle-sports", "nature-trips", "bike-touring", "camping",
                    "surfing", "skiing",
                    "off-road-driving", "rock-climbing", "sea-kayaking", "fly-fishing"]

        for i in range(len(activity)):
            switch = customtkinter.CTkSwitch(self.tab_view_filters.tab("Activities"),
                                             text=activity.__getitem__(i))
            switch.grid(row=math.floor(i / 7), column=i - math.floor(i / 7) * 7, padx=10, pady=(10, 10))
            self.is_on[activity[i]] = False
            self.activity_switches.append(switch)

        # added to the features tab
        self.feature_switches = []

        global features
        features = ["beach", "cave", "city-walk", "forest", "historic-site", "hot-springs", "lake", "partially-paved",
                    "paved", "rails-trails", "river", "views", "waterfall", "wild-flowers", "wildlife"]
        for i in range(len(features)):
            switch = customtkinter.CTkSwitch(self.tab_view_filters.tab("Features"),
                                             text=features.__getitem__(i))
            switch.grid(row=math.floor(i / 8), column=i - math.floor(i / 8) * 8, padx=10, pady=(10, 10))
            self.is_on[features[i]] = False
            self.feature_switches.append(switch)

        # tree view frame
        self.treeview_frame = ttk.Treeview(self, height=18, padding=1, show="headings")
        self.treeview_frame.grid(row=1, column=0, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.treeview_frame['columns'] = list(df_sorted.columns)

        # Create heading columns
        for column in df_sorted.columns:
            self.treeview_frame.heading(column, text=column)

    def add_values_help(self):
        global user_preferences
        total = len(user_preferences)

        if total == 0:
            total = 10
        fraction = float(1 / total) * .95

        for i in range(len(features)):
            if self.feature_switches[i].__getattribute__("_check_state"):
                user_preferences[features[i]] = (1, fraction)

        for i in range(len(activity)):
            if self.activity_switches[i].__getattribute__("_check_state"):
                user_preferences[activity[i]] = (1, fraction)

        if not (self.popularity_entry.get() == ""):
            user_preferences["popularity"] = (int(self.popularity_entry.get()), fraction)

        if not (self.length_entry.get() == ""):
            user_preferences["length"] = (int(self.length_entry.get()), fraction)

        if not (self.elevation_entry.get() == ""):
            user_preferences["elevation_gain"] = (int(self.elevation_entry.get()), fraction)

        if not (self.elevation_entry.get() == ""):
            user_preferences["elevation_gain"] = (int(self.elevation_entry.get()), fraction)

        if not (self.difficulty.get() == "Any Difficulty"):
            user_preferences["difficulty_rating"] = (int(self.difficulty.get()), fraction)

        if not (self.dog_preference.get() == "No Dog Preferences"):
            user_preferences[self.dog_preference.get()] = (1, fraction)

    def run_search(self):
        # Add df rows to treeview
        global user_preferences
        user_preferences = {"loop": (1, 0)}
        self.add_values_help()
        self.add_values_help()

        distance_threshold = 200

        if not (self.radius.get() == ""):
            distance_threshold = int(self.radius.get())
        else:
            distance_threshold = 200

        user_location = {'lat': latitude, 'lng': longitude}

        # get trails data path
        current_directory = os.getcwd()
        trail_data_path = os.path.abspath(os.path.join(current_directory, os.pardir)) + "/data/trails.csv"

        # flow of function calls to return dataframe ranked by user preference

        global df_sorted
        # print(df_sorted)
        reduced_df = pd.DataFrame(columns=["name", "area_name", "city_name", "state_name"])
        if not df_sorted.empty:
            reduced_df = df_sorted[["name", "area_name", "city_name", "state_name"]]

        for item in self.treeview_frame.get_children():
            self.treeview_frame.delete(item)

        for index, row in reduced_df.iterrows():
            self.treeview_frame.insert("", tk.END, values=list(row))

    def input_latitude_and_longitude(self):
        dialog = customtkinter.CTkInputDialog(text="Please enter your zip code",
                                              title="Zip")
        current_directory = os.getcwd()
        zip_data_path = os.path.abspath(os.path.join(current_directory, os.pardir)) + "/data/uszips.csv"

        zip_df = pd.read_csv(zip_data_path)

        try:

            string = dialog.get_input()
            df_output = zip_df.loc[zip_df['zip'] == int(string)]
            geo_loc = np.array((df_output[df_output['zip'] == int(string)][['lat', 'lng']]))
            global latitude
            global longitude
            latitude = float(geo_loc[0][0])
            longitude = float(geo_loc[0][1])
        except ValueError:
            self.input_latitude_and_longitude()




