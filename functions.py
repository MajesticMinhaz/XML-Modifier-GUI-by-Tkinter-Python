import os
import re
from tkinter import Entry
from tkinter import filedialog
from tkinter import messagebox
from tkinter import StringVar


def clear_edit_text(field_name: Entry) -> None:
    return field_name.delete(first=0, last="end")


def browse_file(edit_text: Entry, *field: str):
    clear_edit_text(field_name=edit_text)

    file_path = filedialog.askopenfilename(
        title=field[0],
        filetypes=[(field[1], field[2])]
    )
    if field[3] == "True":
        edit_text.insert(0, os.path.dirname(file_path))
    else:
        edit_text.insert(0, file_path)


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


def edit_text_validator(condition: str, variable: StringVar, edit_text: Entry, err_msg: str) -> bool:
    if not re.fullmatch(pattern=condition, string=variable.get()):
        clear_edit_text(field_name=edit_text)
        err_message_dialog(extra=True, custom_msg=err_msg)
        return False
    else:
        return True
