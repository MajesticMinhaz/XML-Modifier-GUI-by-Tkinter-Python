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
