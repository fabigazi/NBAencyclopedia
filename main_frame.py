import time

import customtkinter
import pymysql
import tkinter

customtkinter.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

app = customtkinter.CTk()
app.geometry("600x600")
app.title("CustomTkinter simple_example.py")

cnx = pymysql.connections

genres = []

frame = customtkinter.CTkFrame(master=app)
frame.pack(pady=20, padx=60, fill="both", expand=True)

input_entry = customtkinter.CTkEntry(master=frame, placeholder_text="Genre")
input_entry.pack(pady=10, padx=10)


def search_button():
    is_in = False
    # input is Stored in variable i
    i = input_entry.get()
    global genres
    # Verifying against the retrieved list rather than testing in sql statement
    for element in genres:
        if element == i:
            is_in = True
    if is_in:
        cur = cnx.cursor()

        stmt_select = "CALL book_has_genre('" + i + "')"

        try:
            cur.execute(stmt_select)
            print("Number of rows %d" % cur.rowcount)

        except pymysql.Error:
            tkinter.messagebox.showerror('SQL Error', 'There was an issue executing the MySQL procedure')
            print('SELECT failed %s Error; %d: %s')
            exit()

        s = ""
        for row in cur.fetchall():
            s += row["title"] + "\n"
        print(s)
        textbox.insert(0.0, s)
        frame.pack()
        cnx.close()
        exit()


    else:
        tkinter.messagebox.showerror('Incorrect Input', 'The given input was not correct or not in the given format')


textbox = customtkinter.CTkTextbox(master=frame, width=400, height=300)
textbox.pack(pady=10, padx=10)

search = customtkinter.CTkButton(master=frame, command=search_button, text="Search")
search.pack(pady=10, padx=10)


def run(var):
    global cnx
    cnx = var
    cur = cnx.cursor()
    stmt_select = "SELECT * FROM genre"

    try:
        cur.execute(stmt_select)
        print("Number of rows %d" % cur.rowcount)

    except pymysql.Error:
        print('SELECT failed %s Error; %d: %s')
        exit()

    s = ""
    global genres

    for row in cur.fetchall():
        s += row["name"] + "\n"
        genres.append(row["name"])

    print(s)
    textbox.insert(0.0, s)
    app.mainloop()
