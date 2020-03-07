from tkinter import Tk, Label, Frame, StringVar, LEFT
from threading import Thread, Event
from collections import namedtuple
from PIL import Image, ImageTk
import os

DashboardTheme = namedtuple('Theme', 'background foreground')

DEFAULT_THEME = DashboardTheme('gray10', 'gray90')
DEFAULT_FONT_SIZE = 300

class Dashboard(Thread):
    """ Thread for the creation and the update of UI objects. """

    def __init__(self, provider, theme=DEFAULT_THEME, font_size=DEFAULT_FONT_SIZE):
        """  Set data provider and graphic interface options. """
        Thread.__init__(self, name="dashboard_thread", daemon=True)
        self.provider = provider
        self.theme = theme
        self.font_size = font_size
        self.icons = { }
        self.end_setup = Event()

    def loadIcons(self):
        """ Populate the icons dictionary with all the rendered icons inside the 'icons' directory. """
        root_dir = os.path.dirname(__file__)
        icons_dir = os.path.join(root_dir, 'icons')
        for file in os.listdir(icons_dir):
            filename = os.fsdecode(file)
            path = os.path.join(icons_dir, filename)
            image = Image.open(path)
            self.icons[filename] = ImageTk.PhotoImage(image)

    def setupGUI(self):
        """ 
        Initialize the main screen.

        The main screen is composed by two areas: 
         - The Display area, where are displayed main info
         - The StatusBar area, where are displayed info about the system status
        """
        self.root = Tk()
        self.root.configure(bg=self.theme.background, cursor='none')
        self.root.attributes('-fullscreen', True)
        self.loadIcons()
        self.setupDisplay()
        self.setupStatusBar()

    def setupDisplay(self):
        """ Setup Display area by creating and placing UI elements. """
        self.speed = StringVar()
        self.heading = StringVar()

        speed_lbl = Label(self.root, textvariable=self.speed, font=('Arial Bold', self.font_size), fg=self.theme.foreground, bg=self.theme.background)
        knots_lbl = Label(self.root, text="kt", font=('Arial Bold', int(self.font_size/2)), fg=self.theme.foreground, bg=self.theme.background)
        heading_lbl = Label(self.root, textvariable=self.heading, font=('Arial Bold', self.font_size), fg=self.theme.foreground, bg=self.theme.background)
        degrees_lbl = Label(self.root, text="°", font=('Arial Bold', self.font_size), fg=self.theme.foreground, bg=self.theme.background)

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)

        speed_lbl.grid(column=0, row=0, sticky='E')
        knots_lbl.grid(column=1, row=0)
        heading_lbl.grid(column=0, row=1, sticky='E')
        degrees_lbl.grid(column=1, row=1)

    def setupStatusBar(self):
        """ Setup StatusBar area by creating and placing UI elements. """
        status_frame = Frame(self.root, bg=self.theme.foreground)
        status_frame.grid(column=0, row=2, columnspan=2, sticky='EW')

        self.gps_icn = Label(status_frame, image=self.icons['gps_disconnected.png'], bg=self.theme.foreground)
        self.gps_icn.image = self.icons['gps_disconnected.png']

        self.gps_icn.pack(side=LEFT)

    def update(self):
        """ Update UI objects accordingly to the provider data. Executed every 500 ms. """
        if self.provider.fix.actual:
            self.speed.set("-" if self.provider.speed.isDefault() else str(self.provider.speed.actual))
            self.heading.set("-" if self.provider.heading.isDefault() else str(self.provider.heading.actual))
            icon = self.icons['gps_connected.png']
        else:
            self.speed.set("-")
            self.heading.set("-")
            icon = self.icons['gps_disconnected.png']

        self.gps_icn.configure(image=icon)
        self.gps_icn.image = icon

        self.root.after(500, self.update)

    def run(self):
        """ Setup the graphics, start the updating process and enter tkinter mainloop. """
        self.setupGUI()
        self.update()
        self.end_setup.set()
        self.root.mainloop()
