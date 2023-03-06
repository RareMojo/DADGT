import os
import threading

class DadgtController:
    """
    Controller for the Dad Game Tools application.
    Acts as a bridge between DADGT and DADGT-App.
    For testing use the EmptyController.
    """
    def __init__(self, dadgtapp, dadgt):
        self.dadgt = dadgt
        self.dadgtapp = dadgtapp
        self.thread = None

    def start(self):
        if self.thread is None or not self.thread.is_alive():
            self.thread = threading.Thread(target=self.dadgt.start)
            self.thread.start()

    def stop(self):
        self.dadgt.stop()
        os._exit(0)

    def on_stop(self):
        self.dadgt.stop()
        # if self.thread is not None:
        #     self.thread.join()  # wait for the thread to finish
        #     self.thread = None  # reset the thread reference

    def update_settings(self):
        self.dadgt.get_settings()

    def update_log(self):
        self.dadgtapp.update_log()

    def restart_ui(self):
        self.dadgtapp.restart_ui()