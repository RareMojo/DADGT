import signal
import tkinter as tk
from tkinter import ttk
import utility.paths as paths
from dadgt import Dadgt


"""
Useful Links:
https://stackoverflow.com/questions/7546050/switch-between-two-frames-in-tkinter Most useful in my opinion
https://www.tutorialspoint.com/python/python_gui_programming.htm
https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/index.html
https://www.youtube.com/watch?v=HjNHATw6XgY&list=PLQVvvaa0QuDclKx-QpC9wntnURXVJqLyk
"""

# You can also use a pandas dataframe for pokemon_info.
# you can convert the dataframe using df.to_numpy.tolist()


frame_styles = {"relief": "groove",
                "bd": 3, "bg": "#3D3D3D",
                "fg": "#9A68E3", "font": ("Verdana", 10, "bold")}


class AppMenuBar(tk.Menu):
    def __init__(self, parent):
        tk.Menu.__init__(self, parent)

        menu_file = tk.Menu(self, tearoff=0)
        self.add_cascade(label="File", menu=menu_file)
        menu_file.add_command(label="MAKE THIS SAVE LOG", command=lambda: parent.show_frame(AppWidgets))
        menu_file.add_separator()
        menu_file.add_command(label="Exit", command=lambda: parent.Quit_application())

class DadgtApp(tk.Tk):

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)

        # Set the style to use the Fusion theme
        style = ttk.Style()
        style.theme_use('clam')

        main_frame = tk.Frame(self, bg="#3D3D3D", height=1024, width=1024)
        main_frame.pack_propagate(0)
        main_frame.pack(fill="both", expand="true")
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        # self.resizable(0, 0) #prevents the app from being resized
        self.geometry("1024x600")# fixes the applications size
        self.frames = {}
        pages = (AppWidgets, PageOne)
        for F in pages:
            frame = F(main_frame, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(AppWidgets)
        menubar = AppMenuBar(self)
        tk.Tk.config(self, menu=menubar)

    def show_frame(self, name):
        frame = self.frames[name]
        frame.tkraise()

    def OpenNewWindow(self):
        OpenNewWindow()

    def Quit_application(self):
        self.destroy()



class AppGUI(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        # Setup main window
        self.main_frame = tk.Frame(self, bg="#3D3D3D", height=600, width=800)
        # self.main_frame.pack_propagate(0)
        self.main_frame.pack(fill="both", expand="true")
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)


class AppWidgets(AppGUI):  # inherits from the GUI class
    def __init__(self, parent, controller):
        AppGUI.__init__(self, parent)

        # Frame setup for main window
        terminal_frame = tk.LabelFrame(self, frame_styles, text="Terminal Log")
        terminal_frame.place(relx=0.02, rely=0.05, relwidth=0.39, relheight=0.8, anchor="nw")

        player_info_frame = tk.LabelFrame(self, frame_styles, text="Player Info")
        player_info_frame.place(relx=0.9, rely=0.05, relwidth=0.39, relheight=0.8, anchor="ne")

        button_frame = tk.LabelFrame(self, frame_styles)
        button_frame.place(relx=0.1, rely=0.97, relwidth=0.2, relheight=0.1, anchor="sw")

        # Setup widgets
        text_frame = tk.Frame(terminal_frame)
        text_frame.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.log_text = tk.Text(text_frame, width=40)
        self.log_text.place(relx=0, rely=0, relwidth=1, relheight=1)
        scrollbar = tk.Scrollbar(text_frame, command=self.log_text.yview)
        scrollbar.place(relx=1, rely=0, relheight=1, anchor='ne')
        self.log_text.config(yscrollcommand=scrollbar.set)

        start_button = tk.Button(button_frame, text="Start", command=None, height=1, width=6)
        start_button.place(relx=0.18, rely=0.5, anchor='w')
        stop_button = tk.Button(button_frame, text="Stop", command=None, height=1, width=6)
        stop_button.place(relx=0.82, rely=0.5, anchor='e')


        def start_dadgt(playerName, monitorNumber, timerInterval):
            dadgt = Dadgt(playerName, monitorNumber, timerInterval)
            signal.signal(signal.SIGTERM, dadgt._signal_handler)
            dadgt._start()


        def Load_data():
            pass

        def Refresh_data():
            Load_data()

        Load_data()


class PageOne(AppGUI):
    def __init__(self, parent, controller):
        AppGUI.__init__(self, parent)

        label1 = tk.Label(self.main_frame, font=("Verdana", 20), text="Page One")
        label1.pack(side="top")


class OpenNewWindow(tk.Tk):

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)

        main_frame = tk.Frame(self)
        main_frame.pack_propagate(0)
        main_frame.pack(fill="both", expand="true")
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        self.title("Here is the Title of the Window")
        self.geometry("500x500")
        self.resizable(0, 0)

        frame1 = ttk.LabelFrame(main_frame, text="This is a ttk LabelFrame")
        frame1.pack(expand=True, fill="both")

        label1 = tk.Label(frame1, font=("Verdana", 20), text="OpenNewWindow Page")
        label1.pack(side="top")




root = DadgtApp()
root.iconbitmap(paths.icon_ico_path)
root.title("DADGT Game Tools")

root.mainloop()