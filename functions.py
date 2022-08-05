"""
===========================================================================================================
                                File        functions.py (Functions Store)
                                Author      Md. Minhaz
                                Email       mdm047767@gmail.com
                                Hire Me     https://pph.me/mdminhaz2003/
                                Repo Link   https://github.com/mdminhaz2003/XML-Modifier-GUI-by-Tkinter-Python
                                Location    Bangladesh
                                Date        04-08-2022 at 22:44:16 (GMT + 6)
===========================================================================================================
"""
import os
import re
from tkinter import Entry
from tkinter import filedialog
from tkinter import messagebox
from tkinter import StringVar
from typing import Literal


def clear_edit_text(text_variable: StringVar) -> None:
    text_variable.set("")


def browse_file(text_variable: StringVar, *field: str):
    clear_edit_text(text_variable=text_variable)

    file_path = filedialog.askopenfilename(
        title=field[0],
        filetypes=[(field[1], field[2])]
    )
    if field[3] == "True":
        text_variable.set(os.path.dirname(file_path))
    else:
        text_variable.set(file_path)


def dropdown_status(dropdown_variable: StringVar) -> str:
    return dropdown_variable.get()


def dropdown_disabled(dropdown):
    dropdown.configure(
        state="disabled"
    )


def err_message_dialog(field_name: str = None, extra: bool = False, custom_msg: str = None) -> None:
    if extra:
        messagebox.showwarning("Error", custom_msg)
    elif not extra:
        messagebox.showwarning("Empty Field", f"{field_name} can't be empty.")
    else:
        messagebox.showwarning("Wrong !", "Something went wrong !")


def edit_text_validator(condition: str, variable: StringVar, err_msg: str) -> bool:
    if not re.fullmatch(pattern=condition, string=variable.get()):
        clear_edit_text(text_variable=variable)
        err_message_dialog(extra=True, custom_msg=err_msg)
        return False
    else:
        return True


def set_config(field_name: Entry, config: Literal["normal", "disabled", "readonly"]) -> None:
    return field_name.config(state=config)


def is_empty(text_variable: StringVar) -> bool:
    return True if len(text_variable.get()).__eq__(0) else False

