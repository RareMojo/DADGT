class Settings:
    """
    Settings class for the dadgtapp to save and load settings for dadgt
    """
    def __init__(self):
        # Default settings
        self.monitorNumber = 1
        self.timerInterval = 0.5
        self.playerName = "Player"
        self.lobbyCode = "1234"
        self.serverName = "localhost"

    def set_monitor_number(self, number):
        self.monitorNumber = number

    def set_timer_interval(self, interval):
        self.timerInterval = interval
    
    def set_player_name(self, name):
        self.playerName= name

    def set_lobby_code(self, code):
        self.lobbyCode = code

    def set_server_name(self, name):
        self.serverName = name

    def get_monitor_number(self):
        return self.monitorNumber
    
    def get_timer_interval(self):
        return self.timerInterval
    
    def get_player_name(self):
        return self.playerName
    
    def get_lobby_code(self):
        return self.lobbyCode
    
    def get_server_name(self):
        return self.serverName