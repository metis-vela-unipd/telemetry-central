from flask import Flask, render_template
from flask_socketio import SocketIO
from threading import Thread, Event
from colorama import Style

class Webapp(Thread):

    def __init__(self, provider):
        Thread.__init__(self, name="webapp_thread", daemon=True)
        self.app = Flask(__name__)
        self.app.config['SECRET_KEY'] = 'f7acbeb708f93e5e81e8a55238aae4bbc75f69ac36d18d0c'
        self.socketio = SocketIO(self.app)

        self.app.add_url_rule('/', 'index', self.index)

        self.provider = provider
        self.end_setup = Event()

    def index(self):
        return render_template('index.html', speed=self.provider.speed.actual, heading=self.provider.heading.actual)

    def update(self):
        while True:
            self.socketio.sleep(0.5)
            self.socketio.emit('update', {'speed': self.provider.speed.actual, 'heading': self.provider.heading.actual})

    def run(self):
        self.socketio.start_background_task(self.update)

        print(f"{Style.DIM}[{self.getName()}] Setup finished{Style.RESET_ALL}")
        self.end_setup.set()

        self.socketio.run(self.app)
