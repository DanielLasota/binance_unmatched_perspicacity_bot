from flask import Flask, Response
from flask_cors import CORS
import time
import json
import logging
from threading import Thread, Event


class FlaskManager:
    def __init__(self):
        self.app = Flask(__name__)
        CORS(self.app)
        self.setup_routes()
        self.current_data = {"message": "Initial data"}
        self.data_updated = Event()
        log = logging.getLogger('werkzeug')
        log.setLevel(logging.ERROR)

    def setup_routes(self):
        @self.app.route('/time_stream')
        def time_stream():
            return Response(self.stream(), mimetype='text/event-stream')
            
    def stream(self):
        while True:
            self.data_updated.wait()
            data = self.current_data
            yield f"data: {json.dumps(data)}\n\n"
            self.data_updated.clear()

    def update(self, variable, message):
        self.current_data = {variable: message}
        
        if variable == 'transaction':
            self.current_data = {variable: f'{message.price}   {message.market_order_side}'}
        self.data_updated.set()

    def app_init(self):
        self.app.run(threaded=True, debug=False)
        
    def run(self):
        daemon_thread = Thread(target=self.app_init)
        daemon_thread.daemon = True
        daemon_thread.start()

