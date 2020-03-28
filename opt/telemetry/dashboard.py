#  Copyright (c) 2020 Matteo Carnelos.
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.

from tkinter import Tk, Label, Frame, StringVar, LEFT
from threading import Thread, Event
from collections import namedtuple
from PIL import Image, ImageTk
from colorama import Style
import os

DashboardTheme = namedtuple('Theme', 'background foreground')

DEFAULT_THEME = DashboardTheme('gray10', 'gray90')
DEFAULT_FONT_SIZE = 300


class Dashboard(Thread):
    """ Thread for the creation and the update of UI objects. """

    def __init__(self, provider, logger, theme=DEFAULT_THEME, font_size=DEFAULT_FONT_SIZE):
        """  Set data provider and graphic interface options. """
        Thread.__init__(self, name="dashboard_thread", daemon=True)
        self.logger = logger
        self.gps = provider.getSensor('gps')
        self.theme = theme
        self.font_size = font_size
        self.icons = {}
        self.end_setup = Event()
        self.root = None
        self.speed = None
        self.heading = None
        self.gps_icn = None
        self.log_icn = None
        self.log_lbl = None

    def load_icons(self):
        """ Populate the icons dictionary with all the rendered icons inside the 'icons' directory. """
        root_dir = os.path.dirname(__file__)
        icons_dir = os.path.join(root_dir, 'icons')
        for file in os.listdir(icons_dir):
            filename = os.fsdecode(file)
            path = os.path.join(icons_dir, filename)
            image = Image.open(path)
            self.icons[filename] = ImageTk.PhotoImage(image)

    def setup_gui(self):
        """ 
        Initialize the main screen.

        The main screen is composed by two areas: 
         - The Display area, where are displayed main info
         - The StatusBar area, where are displayed info about the system status
        """
        self.root = Tk()
        self.root.configure(bg=self.theme.background, cursor='none')
        self.root.attributes('-fullscreen', True)
        self.load_icons()
        self.setup_display()
        self.setup_statusbar()

    def setup_display(self):
        """ Setup Display area by creating and placing UI elements. """
        self.speed = StringVar()
        self.heading = StringVar()

        speed_lbl = Label(self.root,
                          textvariable=self.speed,
                          font=('Arial Bold', self.font_size),
                          fg=self.theme.foreground,
                          bg=self.theme.background)
        knots_lbl = Label(self.root,
                          text="kt",
                          font=('Arial Bold', int(self.font_size/2)),
                          fg=self.theme.foreground,
                          bg=self.theme.background)
        heading_lbl = Label(self.root,
                            textvariable=self.heading,
                            font=('Arial Bold', self.font_size),
                            fg=self.theme.foreground,
                            bg=self.theme.background)
        degrees_lbl = Label(self.root,
                            text="°",
                            font=('Arial Bold', self.font_size),
                            fg=self.theme.foreground,
                            bg=self.theme.background)

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)

        speed_lbl.grid(column=0, row=0, sticky='E')
        knots_lbl.grid(column=1, row=0)
        heading_lbl.grid(column=0, row=1, sticky='E')
        degrees_lbl.grid(column=1, row=1)

    def setup_statusbar(self):
        """ Setup StatusBar area by creating and placing UI elements. """
        status_frame = Frame(self.root, bg=self.theme.foreground)
        status_frame.grid(column=0, row=2, columnspan=2, sticky='EW')

        self.gps_icn = Label(status_frame,
                             image=self.icons['gps_disconnected.png'],
                             bg=self.theme.foreground)
        self.gps_icn.image = self.icons['gps_disconnected.png']
        self.log_icn = Label(status_frame,
                             image=self.icons['logging.png'],
                             bg=self.theme.foreground)
        self.log_icn.image = self.icons['logging.png']
        self.log_lbl = Label(status_frame,
                             text="LOGGING...",
                             font=('Arial Bold', 16),
                             fg='red4',
                             bg=self.theme.foreground)

        self.gps_icn.pack(side=LEFT)

    def update(self):
        """ Update UI objects accordingly to the provider data. Executed every 500 ms. """
        self.speed.set(self.gps.speed_display)
        self.heading.set(self.gps.heading_display)
        if self.gps.has_fix:
            icon = self.icons['gps_connected.png']
        else:
            icon = self.icons['gps_disconnected.png']

        if self.logger.is_logging:
            self.log_icn.pack(side=LEFT)
            self.log_lbl.pack(side=LEFT)
        else:
            self.log_icn.pack_forget()
            self.log_lbl.pack_forget()

        self.gps_icn.configure(image=icon)
        self.gps_icn.image = icon

        self.root.after(500, self.update)

    def run(self):
        """ Setup the graphics, start the updating process and enter tkinter mainloop. """
        self.setup_gui()
        self.update()
        print(f"{Style.DIM}[{self.getName()}] Setup finished{Style.RESET_ALL}")
        self.end_setup.set()
        self.root.mainloop()
