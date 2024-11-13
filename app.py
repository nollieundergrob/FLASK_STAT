from flask import Flask, render_template
from flask_socketio import SocketIO
import psutil
import time
import threading

app = Flask(__name__)
socketio = SocketIO(app)

def background_thread():
    while True:
        time.sleep(0.3)
        cpu = psutil.cpu_percent()
        memory = psutil.virtual_memory().percent
        socketio.emit('update', {'cpu': cpu, 'memory': memory})

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    thread = threading.Thread(target=background_thread)
    thread.start()
    socketio.run(app, host='0.0.0.0', port=5000)