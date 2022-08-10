"""
===========================================================================================================
                                File        xml_modifier.py (Entry point)
                                Author      Md. Minhaz
                                Email       mdm047767@gmail.com
                                Hire Me     https://pph.me/mdminhaz2003/
                                Repo Link   https://github.com/mdminhaz2003/XML-Modifier-GUI-by-Tkinter-Python
                                Location    Bangladesh
                                Date        31-07-2022 at 16:01:00 (GMT + 6)
===========================================================================================================
"""
from tkinter import Tk
from tkinter import Canvas
from tkinter import LEFT
from tkinter import BOTH
from tkinter import YES
from tkinter import VERTICAL
from tkinter import RIGHT
from tkinter import Y
from tkinter import Frame
from tkinter.ttk import Scrollbar
from widgets import Widgets
from app import Ui

if __name__ == '__main__':
    root = Tk()
    root.configure(background="gray20")
    root.title("XML Modifier")
    root.resizable(width=False, height=False)
    label_frame = Frame(master=root, background="gray20")
    label_frame.grid(row=0, column=0, padx=10, pady=10)

    canvas = Canvas(master=label_frame, width=1125, height=640, background="gray20")
    canvas.pack(side=LEFT, fill=BOTH, expand=YES)
    y_scroll_bar = Scrollbar(master=label_frame, orient=VERTICAL, command=canvas.yview)
    y_scroll_bar.pack(side=RIGHT, fill=Y, padx=5, pady=5)
    canvas.configure(yscrollcommand=y_scroll_bar.set)
    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
    my_frame = Frame(canvas, background="gray20")
    widgets = Widgets(master=my_frame)
    canvas.create_window((0, 0), window=my_frame, anchor="nw")
    ui = Ui(master=widgets)
    ui.widget_packer()
    root.mainloop()
