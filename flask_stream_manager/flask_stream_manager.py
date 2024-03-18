from flask import Flask, Response, request
from flask_cors import CORS
import time
import json
import logging
from threading import Thread, Event
from queue import Queue

from abstract_base_classes.observer import Observer


class FlaskManager(Observer):
    def __init__(self):
        super().__init__()
        self.observers = []
        self.app = Flask(__name__)
        CORS(self.app)
        self.setup_routes()
        self.data_queue = Queue()
        self.data_updated = Event()
        log = logging.getLogger('werkzeug')
        log.setLevel(logging.ERROR)

    def update(self, message):
        self.data_queue.put(message)
        self.data_updated.set()

    def setup_routes(self):
        @self.app.route('/time_stream')
        def main_stream():
            return Response(self.stream(), mimetype='text/event-stream')

        @self.app.route('/post', methods=['POST'])
        def receive_data():
            data = request.get_json()
            print(f'>> {list(data.items())[0][1]}')
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