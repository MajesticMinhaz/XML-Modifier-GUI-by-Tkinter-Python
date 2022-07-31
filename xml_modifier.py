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


if __name__ == '__main__':
    root = Tk()
    root.configure(
        background="gray20",
        padx=10,
        pady=10
    )
    root.title("XML Modifier")
    root.resizable(width=False, height=False)

    canvas = Canvas(
        master=root,
        background="gray20",
        border=10,
        width=780,
        height=640
    )
    canvas.pack(
        side=LEFT,
        fill=BOTH,
        expand=YES
    )

    root.mainloop()
