from flask import Flask, Response, request
from flask_cors import CORS
import time
import json
import logging
from threading import Thread, Event
from queue import Queue


class FlaskManager:
    def __init__(self):
        self.observers = []
        self.app = Flask(__name__)
        CORS(self.app)
        self.setup_routes()
        self.data_queue = Queue()
        self.data_updated = Event()
        log = logging.getLogger('werkzeug')
        log.setLevel(logging.ERROR)

    def subscribe(self, observer):
        self.observers.append(observer)

    def unsubscribe(self, observer):
        self.observers.remove(observer)

    def notify_observers(self, data):
        for observer in self.observers:
            observer.update(data)

    def update(self, variable, message):
        data = {variable: message}
        self.data_queue.put(data)
        self.data_updated.set()

    def setup_routes(self):
        @self.app.route('/time_stream')
        def main_stream():
            return Response(self.stream(), mimetype='text/event-stream')

        @self.app.route('/post', methods=['POST'])
        def receive_data():
            data = request.get_json()
            print('received sth')
            print(data)
            self.notify_observers(data)
            return "Data received"

    def stream(self):
        while True:
            self.data_updated.wait()
            while not self.data_queue.empty():
                data = self.data_queue.get()
                yield f"data: {json.dumps(data)}\n\n"
            self.data_updated.clear()

    def app_init(self):
        self.app.run(threaded=True, debug=False)

    def run(self):
        daemon_thread = Thread(target=self.app_init)
        daemon_thread.daemon = True
        daemon_thread.start()