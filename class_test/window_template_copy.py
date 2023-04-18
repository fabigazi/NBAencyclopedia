import math

import customtkinter
import pymysql
import tkinter as tk
from tkinter import *
from tkinter import messagebox, ttk
import pandas as pd
from PIL import Image, ImageTk

from window import Window


def open_window(cnx, cur, root):
    customtkinter.set_appearance_mode("Light")  # Modes: "System" (standard), "Dark", "Light"
    customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

    # Create new window
    wn = Toplevel(root)
    frame3 = Frame(wn)

    # Set window specifications and location
    window_width = 1145
    window_height = 675
    screen_width = wn.winfo_screenwidth()
    screen_height = wn.winfo_screenheight()
    x_coor = screen_width / 2 - window_width / 2
    y_coor = screen_height / 2 - window_height / 2
    wn.geometry("%dx%d+%d+%d" % (window_width, window_height, x_coor, y_coor))

    # initialize variables
    is_on = {}
    df_sorted = df = pd.DataFrame({'name': pd.Series(dtype='str'),
                                   'area_name': pd.Series(dtype='str'),
                                   'city_name': pd.Series(dtype='str'),
                                   'state_name': pd.Series(dtype='str')})

    df_sorted = df_sorted[['name', 'area_name', 'city_name', 'state_name']]
    df_sorted = df_sorted.rename(
        columns={'name': 'Trail Name', 'area_name': 'Area', 'city_name': 'City', 'state_name': 'State'})

    # Createing widgets
    tab_view_filters = customtkinter.CTkTabview(frame3, width=1110, height=230)
    tab_view_filters.grid(row=0, column=0, padx=(20, 0), pady=(20, 0), sticky="nsew")
    tab_view_filters.add("Trail Preferences")
    tab_view_filters.add("Features")
    tab_view_filters.add("Activities")
    tab_view_filters.tab("Trail Preferences").grid_columnconfigure(3, weight=1)  # configure grid of

    # individual tabs
    tab_view_filters.tab("Features").grid_columnconfigure(0, weight=1)

    # tabview.tab("tabX") assigns the obect to the given tabX tab
    popularity_entry = customtkinter.CTkEntry(tab_view_filters.tab("Trail Preferences"),
                                              placeholder_text="Popularity 0-85")
    popularity_entry.grid(row=0, column=0, padx=20, pady=(10, 10))
    # TODO: mi -> ft
    length_entry = customtkinter.CTkEntry(tab_view_filters.tab("Trail Preferences"),
                                          placeholder_text="length in ft")
    length_entry.grid(row=0, column=1, padx=20, pady=(10, 10))

    elevation_entry = customtkinter.CTkEntry(tab_view_filters.tab("Trail Preferences"),
                                             placeholder_text="elevation in ft")
    elevation_entry.grid(row=0, column=2, padx=20, pady=(10, 10))

    # slider_1 = customtkinter.CTkSlider(tab_view_filters.tab("Trail Preferences"), from_=0, to=1,
    #                                       number_of_steps=4)
    # slider_1.grid(row=0, column=3, padx=(20, 10), pady=(10, 10), sticky="ew")

    difficulty = customtkinter.CTkOptionMenu(tab_view_filters.tab("Trail Preferences"),
                                             dynamic_resizing=True,
                                             values=["Any Difficulty", "1", "2", "3", "4", "5"])

    difficulty.grid(row=0, column=3, padx=20, pady=(10, 10))

    radius = customtkinter.CTkEntry(tab_view_filters.tab("Trail Preferences"),
                                    placeholder_text="Search Radius in mi")
    radius.grid(row=0, column=4, padx=20, pady=(10, 10))

    dog_preference = customtkinter.CTkOptionMenu(tab_view_filters.tab("Trail Preferences"),
                                                 dynamic_resizing=True,
                                                 values=["No Dog Preferences", "dogs", "dogs-leash",
                                                         "dogs-no"])

    dog_preference.grid(row=0, column=5, padx=20, pady=(10, 10))

    search_button = customtkinter.CTkButton(tab_view_filters.tab("Trail Preferences"), text="Search",
                                            command=run_search)
    search_button.grid(row=4, column=5, padx=20, pady=(10, 10))

    search_button1 = customtkinter.CTkButton(tab_view_filters.tab("Features"), text="Search",
                                             command=run_search)
    search_button1.grid(row=3, column=7, padx=20, pady=(10, 10))

    search_button2 = customtkinter.CTkButton(tab_view_filters.tab("Activities"), text="Search",
                                             command=run_search)
    search_button2.grid(row=3, column=6, padx=20, pady=(10, 10))

    # added to the activity tab
    activity_switches = []

    global activity
    activity = ["cross-country-skiing", "mountain-biking", "trail-running", "snowboarding",
                "road-biking", "fishing", "walking",
                "whitewater-kayaking", "scenic-driving", "ice-climbing", "backpacking",
                "canoeing", "birding", "hiking",
                "horseback-riding", "paddle-sports", "nature-trips", "bike-touring", "camping",
                "surfing", "skiing",
                "off-road-driving", "rock-climbing", "sea-kayaking", "fly-fishing"]

    for i in range(len(activity)):
        switch = customtkinter.CTkSwitch(tab_view_filters.tab("Activities"),
                                         text=activity.__getitem__(i))
        switch.grid(row=math.floor(i / 7), column=i - math.floor(i / 7) * 7, padx=10, pady=(10, 10))
        is_on[activity[i]] = False
        activity_switches.append(switch)

    # added to the features tab
    feature_switches = []

    global features
    features = ["beach", "cave", "city-walk", "forest", "historic-site", "hot-springs", "lake", "partially-paved",
                "paved", "rails-trails", "river", "views", "waterfall", "wild-flowers", "wildlife"]
    for i in range(len(features)):
        switch = customtkinter.CTkSwitch(tab_view_filters.tab("Features"),
                                         text=features.__getitem__(i))
        switch.grid(row=math.floor(i / 8), column=i - math.floor(i / 8) * 8, padx=10, pady=(10, 10))
        is_on[features[i]] = False
        feature_switches.append(switch)

    # tree view frame
    treeview_frame = ttk.Treeview(frame3, height=18, padding=1, show="headings")
    treeview_frame.grid(row=1, column=0, padx=(20, 0), pady=(20, 0), sticky="nsew")
    treeview_frame['columns'] = list(df_sorted.columns)

    # Create heading columns
    for column in df_sorted.columns:
        treeview_frame.heading(column, text=column)

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