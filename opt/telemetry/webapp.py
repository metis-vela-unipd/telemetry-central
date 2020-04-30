from flask import Flask, render_template
from flask_socketio import SocketIO
from threading import Thread, Event
from colorama import Style


class Webapp(Thread):
    """ Thread for the management of the webapp. """

    def __init__(self, provider, logger):
        """ Initialize web framework, set provider and routing.  """
        Thread.__init__(self, name="webapp_thread", daemon=True)
        self.app = Flask(__name__)
        self.app.config['SECRET_KEY'] = 'f7acbeb708f93e5e81e8a55238aae4bbc75f69ac36d18d0c'
        self.socket = SocketIO(self.app)

        self.app.add_url_rule('/', 'index', self.index)
        self.app.add_url_rule('/view', 'view', self.view)
        self.socket.on_event('log_btn_click', self.log_btn_click)

        self.provider = provider
        self.gps = provider.get_sensor('gps')
        self.logger = logger
        self.end_setup = Event()

    def index(self):
        """ Index page handler. Simply render the 'control.html' template in the 'templates' folder. """
        return render_template('control.html',
                               speed=self.gps.speed_display,
                               heading=self.gps.heading_display,
                               fix=self.gps.has_fix,
                               logging=self.logger.is_logging)

    def view(self):
        """ View page handler. Render the 'view.html' file, a special version of the index page without controls. """
        return render_template('view.html')

    def log_btn_click(self):
        """ Event fired when the log button is pressed in the webapp. """
        if self.logger.is_logging:
            self.logger.stop_log()
        else:
            self.logger.start_log()

    def update(self):
        """ Background task for updating live data. Emit a websocket event with updates. """
        while True:
            self.socket.sleep(0.5)
            self.socket.emit('update', {
                'speed': self.gps.speed_display,
                'heading': self.gps.heading_display,
                'fix': self.gps.has_fix,
                'logging': self.logger.is_logging
            })

    def run(self):
        """ Start update task and enter WSGI server (eventlet) main loop. """
        self.socket.start_background_task(self.update)

        print(f"{Style.DIM}[{self.getName()}] Setup finished{Style.RESET_ALL}")
        self.end_setup.set()

        self.socket.run(self.app)
