from flask import Flask, render_template
from flask_socketio import SocketIO
import psutil
import time
import threading

app = Flask(__name__)
socketio = SocketIO(app)

def background_thread():
    while True:
        time.sleep(0.5)
        # Получаем информацию о CPU и памяти
        cpu = psutil.cpu_percent()
        memory = psutil.virtual_memory().percent
        
        # Получаем информацию о сетевых интерфейсах
        net_io = psutil.net_io_counters()
        net_connections = psutil.net_connections(kind='inet')
        
        # Создаем список соединений
        connections = []
        for conn in net_connections:
            connections.append({
                'local_address': conn.laddr,
                'remote_address': conn.raddr,
                'status': conn.status,
                'pid': conn.pid
            })
        
        # Отправляем обновления через SocketIO
        socketio.emit('update', {
            'cpu': cpu,
            'memory': memory,
            'bytes_sent': net_io.bytes_sent,
            'bytes_recv': net_io.bytes_recv,
            'conn': connections,
            'lenght_conn':len(connections)
        })

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    thread = threading.Thread(target=background_thread)
    thread.start()
    socketio.run(app, host='0.0.0.0', port=5000)