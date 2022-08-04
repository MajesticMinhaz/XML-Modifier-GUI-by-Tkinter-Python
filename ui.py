"""
===========================================================================================================
                                File        ui.py (Entry point)
                                Author      Md. Minhaz
                                Email       mdm047767@gmail.com
                                Hire Me     https://pph.me/mdminhaz2003/
                                Repo Link   https://github.com/mdminhaz2003/XML-Modifier-GUI-by-Tkinter-Python
                                Location    Bangladesh
                                Date        04-08-2022 at 22:40:58 (GMT + 6)
===========================================================================================================
"""
from widgets_info import widgets_info
from widgets import Widgets


class Ui:
    def __init__(self, master: Widgets):
        self.master = master

        self.app = {}

    def edit_text_packer(self) -> None:
        for key, value in zip(widgets_info.keys(), widgets_info.values()):
            if value.get("no_need_pack") is None:
                self.app[key] = self.master.edit_text(manager=value)
