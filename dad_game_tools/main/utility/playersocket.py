import socketio

sio = socketio.Client()
lobby = None

@sio.event(namespace='/lobby')
def connect():
    print('connection established to web lobby')

@sio.event(namespace="/lobby")
def disconnect():
    print('disconnected from web lobby')

@sio.event(namespace="/lobby")
def send_info(data):
    data['map'] = data['map'].split("\\")[-1].split(".")[0]
    data['lobby'] = lobby
    sio.emit('position_info', data, namespace='/lobby')

def stop():
    sio.disconnect()

def start(url):
    sio.connect(url)