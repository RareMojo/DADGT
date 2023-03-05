import shutil
import subprocess
import tkinter as tk
from tkinter import ttk

import utility.debug as debug
import utility.paths as paths
from controller.dadgt_controller import DadgtController
from dadgt import Dadgt
from settings import Settings

# Styling options
frame_styles = {"relief": "groove",
                "bd": 3, "bg": "#3D3D3D",
                "fg": "#9A68E3", "font": ("Verdana", 11, "bold")}

label_styles = {"bd": 3, "bg": "#3D3D3D",
                "fg": "#9A68E3", "font": ("Verdana", 8, "bold")}

entry_styles = {"bd": 3, "bg": "#ffffff",
                "fg": "#000000", "font": ("Arial", 10)}


class AppMenuBar(tk.Menu):
    def __init__(self, parent, app_gui, settings):
        tk.Menu.__init__(self, parent)

        self.app_gui = app_gui  # store the app_gui instance
        self.settings = settings

        # File menu
        menu_file = tk.Menu(self, tearoff=0)
        self.add_cascade(label="File", menu=menu_file)
        menu_file.add_command(label="Settings", command=self.show_settings_window)
        menu_file.add_separator()
        menu_file.add_command(label="Save current log", command=lambda: shutil.copyfile(paths.log_path, paths.latest_log_path))
        menu_file.add_separator()
        menu_file.add_command(label="Open latest log", command=lambda: subprocess.Popen(["notepad.exe", paths.latest_log_path]))
        menu_file.add_separator()
        menu_file.add_command(label="Exit", command=self.app_gui.on_close)

        # Create settings menu
    def show_settings_window(self):
        SettingsWindow(self.app_gui, self.settings)


class SettingsWindow(tk.Toplevel):
    def __init__(self, app_gui, settings):
        tk.Toplevel.__init__(self)

        self.app_gui = app_gui
        self.settings = settings

        # Create settings window and title/main frame
        window_frame = tk.Frame(self, bg="#3D3D3D", height=200, width=300)
        window_frame.pack(fill="both", expand="true")
        self.resizable(0, 0)
        self.geometry("300x200")
        self.title("DADGT Settings")
        settings_frame = tk.LabelFrame(window_frame, frame_styles, text="Settings")
        settings_frame.place(relx=0.5, rely=0.5, relwidth=0.925, relheight=0.925, anchor="center")

        # Create entries frame
        entries_frame = tk.LabelFrame(settings_frame, relief="flat", bg="#3D3D3D")
        entries_frame.place(relx=0.5, rely=0.015, relwidth=0.925, relheight=0.7, anchor="n")

        # Create dropdown menus
        monitor_options = [0, 1, 2]
        self.monitorNumber = tk.IntVar(value=settings.monitorNumber)
        monitor_menu = ttk.Combobox(entries_frame, values=monitor_options, textvariable=self.monitorNumber)
        monitor_menu.place(relx=0.65, rely=0.225, relwidth=0.2, anchor="center")
        
        refresh_options = [0.1, 0.5, 1]
        self.timerInterval= tk.IntVar(value=settings.timerInterval)
        refresh_menu = ttk.Combobox(entries_frame, values=refresh_options, textvariable=self.timerInterval)
        refresh_menu.place(relx=0.65, rely=0.525, relwidth=0.2, anchor="center")

        # Create buttons frame
        settings_buttons_frame = tk.LabelFrame(settings_frame, bg="#3D3D3D")
        settings_buttons_frame.place(relx=0.5, rely=0.95, relwidth=0.45, relheight=0.3, anchor="s")

        # Create settings labels
        monitor_label = tk.Label(entries_frame, label_styles, text="Monitor:")
        monitor_label.place(relx=0.225, rely=0.16, anchor='w')
        refresh_label = tk.Label(entries_frame, label_styles, text="Refresh\n      rate:")
        refresh_label.place(relx=0.225, rely=0.51, anchor='w')

        # Create buttons
        save_button = tk.Button(settings_buttons_frame, text="  Save  ", command=self.save_settings)
        save_button.place(relx=0.25, rely=0.5, anchor="center")
        cancel_button = tk.Button(settings_buttons_frame, text="Cancel", command=self.destroy)
        cancel_button.place(relx=0.75, rely=0.5, anchor="center")

    def save_settings(self):
        """
        This function saves the settings to the settings file and closes the settings window.
        """
        monitor_number = self.monitorNumber.get()
        timer_interval = self.timerInterval.get()
        self.settings.set_monitor_number(monitor_number)
        self.settings.set_timer_interval(timer_interval)
        self.monitorNumber.set(monitor_number)
        self.timerInterval.set(timer_interval)
        self.destroy()


class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.settings = Settings()

        # Create main window and title/main frame
        self.frames = {}
        main_frame = tk.Frame(self, bg="#3D3D3D", height=1024, width=512)
        main_frame.pack(fill="both", expand="true")
        self.resizable(0, 0)
        self.geometry("600x480")
        widgets = AppGUI(main_frame, self.settings)
        self.frames[AppGUI] = widgets
        widgets.grid(row=0, column=0, sticky="nsew")
        self.show_frame(AppGUI)
        menubar = AppMenuBar(self, widgets, self.settings)
        tk.Tk.config(self, menu=menubar)

    def show_frame(self, name):
        """
        This function is called to show a frame for the given page name.
        """
        frame = self.frames[name]
        frame.tkraise()

    def on_close(self):
        """
        This function is called when the window is closed.
        """
        self.frames[AppGUI].on_close()


class AppGUI(tk.Frame):
    def __init__(self, parent, settings):
        tk.Frame.__init__(self, parent)

        self.controller = None
        self.settings = settings

        # Main frame setup
        self.main_frame = tk.Frame(self, bg="#3D3D3D", height=600, width=800)
        self.main_frame.pack(fill="both", expand="true")

        # Two frames on top of each other inside main frame
        top_frame = tk.LabelFrame(self, frame_styles, text="Terminal Log")
        top_frame.place(relx=0.372, rely=0.02, relwidth=0.7, relheight=0.55, anchor="n")
        bottom_frame = tk.LabelFrame(self, frame_styles, text="Options")
        bottom_frame.place(relx=0.31, rely=0.765, relwidth=0.5, relheight=0.175, anchor="s")

        # Top frame setup
        text_frame = tk.Frame(top_frame)
        text_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.txt_log = tk.Text(text_frame, width=40)
        self.txt_log.configure(state=tk.DISABLED)
        scrollbar = tk.Scrollbar(text_frame, command=self.txt_log.yview)
        self.txt_log.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.txt_log.configure(yscrollcommand=scrollbar.set)

        # Bottom frame within main frame
        button_frame = tk.LabelFrame(self, frame_styles)
        button_frame.place(relx=0.685, rely=0.683, relwidth=0.1, relheight=0.16, anchor="e")

        # Buttons within button frame
        start_button = tk.Button(button_frame, text="Start", command=lambda: self.on_start(), height=1, width=6)
        start_button.place(relx=0.52, rely=0.15, anchor='n')
        stop_button = tk.Button(button_frame, text="Stop", command=lambda: self.controller.on_stop(), height=1, width=6)
        stop_button.place(relx=0.52, rely=0.875, anchor='s')

        # Input frame within bottom frame
        input_frame = tk.LabelFrame(bottom_frame, relief="flat", bg="#3D3D3D")
        input_frame.place(relx=0.525, rely=0.5, relwidth=0.8, relheight=1, anchor="center")

        # Input labels within input frame
        playerName_label = tk.Label(input_frame, label_styles, text="Player:")
        playerName_label.place(relx=0.015, rely=0.12, anchor='w')
        lobbyCode_label = tk.Label(input_frame, label_styles, text="Lobby:")
        lobbyCode_label.place(relx=0.015, rely=0.42, anchor='w')
        serverName_label = tk.Label(input_frame, label_styles, text="Server:")
        serverName_label.place(relx=0.015, rely=0.72, anchor='w')

        # Input fields within input frame
        self.playerName_entry = tk.Entry(input_frame, entry_styles)
        self.playerName_entry.place(relx=0.9, rely=0.168, relwidth=0.7, anchor='e')
        self.playerName_entry.insert(0, "Player")
        self.lobbyCode_entry = tk.Entry(input_frame, entry_styles)
        self.lobbyCode_entry.place(relx=0.9, rely=0.468, relwidth=0.7, anchor='e')
        self.lobbyCode_entry.insert(0, "420")
        self.serverName_entry = tk.Entry(input_frame, entry_styles)
        self.serverName_entry.place(relx=0.9, rely=0.768, relwidth=0.7, anchor='e')
        self.serverName_entry.insert(0, "http://bmbros.sytes.net:5001/lobby")

        # Set up controller and load settings
        dadgt = Dadgt(self, settings)
        controller = DadgtController(self, dadgt)
        self.controller = controller

    def save_options(self):
        """
        Saves all settings from GUI to settings class.
        """
        playerName = self.playerName_entry.get()
        lobbyCode = self.lobbyCode_entry.get()
        serverName = self.serverName_entry.get()
        self.settings.set_player_name(playerName)
        self.settings.set_lobby_code(lobbyCode)
        self.settings.set_server_name(serverName)

    def update_log(self):
        """
        Called from controller. Updates the log with the contents of the log file.
        """
        with open(paths.log_path, "r") as f:
            log_contents = f.read()
        self.txt_log.configure(state=tk.NORMAL)
        self.txt_log.delete("1.0", tk.END)
        self.txt_log.insert(tk.END, log_contents)
        self.txt_log.configure(state=tk.DISABLED)
        self.txt_log.see(tk.END)

    def clear_log(self):
        """
        Called from controller. Clears the log file and the log text box.
        """
        self.txt_log.configure(state=tk.NORMAL)
        self.txt_log.delete('1.0', tk.END)
        self.txt_log.configure(state=tk.DISABLED)

    def on_start(self):
        """
        Sends controller start command from GUI and saves options.
        """
        self.save_options()
        self.controller.start()

    def on_close(self):
        """
        Exits the GUI program.
        """
        self.clear_log()
        self.controller.stop()


root = App()
root.iconbitmap(paths.icon_ico_path)
root.title("DADGT Game Tools")
root.mainloop()

