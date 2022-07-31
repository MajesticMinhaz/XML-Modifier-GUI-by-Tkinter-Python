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
from tkinter.ttk import LabelFrame


if __name__ == '__main__':
    root = Tk()
    root.title("XML Modifier")
    root.resizable(width=False, height=False)

    label_frame = LabelFrame(
        master=root,
        text="XML Modifier",
        padding=10,
        border=2
    )

    label_frame.grid(
        row=0,
        column=0,
        padx=10,
        pady=10
    )

    root.mainloop()
