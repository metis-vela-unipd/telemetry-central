from tkinter import Tk, Label
import sys

FONT_SIZE = 300
BG_COLOR = 'gray5'
FG_COLOR = 'white'

if '--light' in sys.argv or '-l' in sys.argv:
    BG_COLOR = 'gray90'
    FG_COLOR = 'black'

try:
    if '--size' in sys.argv:
        FONT_SIZE = int(sys.argv[sys.argv.index('--size')+1])
    elif '-s' in sys.argv:
        FONT_SIZE = int(sys.argv[sys.argv.index('-s')+1])
except: FONT_SIZE = 300

root = Tk()
root.configure(bg=BG_COLOR)
root.attributes('-fullscreen', True)

speed_lbl = Label(root, text='2', font=('Arial Bold', FONT_SIZE), fg=FG_COLOR, bg=BG_COLOR)
knots_lbl = Label(root, text='kt', font=('Arial Bold', int(FONT_SIZE/2)), fg=FG_COLOR, bg=BG_COLOR)
heading_lbl = Label(root, text='149', font=('Arial Bold', FONT_SIZE), fg=FG_COLOR, bg=BG_COLOR)
degrees_lbl = Label(root, text='°', font=('Arial Bold', FONT_SIZE), fg=FG_COLOR, bg=BG_COLOR)

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
root.rowconfigure(1, weight=1)

speed_lbl.grid(column=0, row=0, sticky="E")
knots_lbl.grid(column=1, row=0)
heading_lbl.grid(column=0, row=1, sticky="E")
degrees_lbl.grid(column=1, row=1)

root.mainloop()