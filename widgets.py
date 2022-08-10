"""
===========================================================================================================
                                File        widgets.py (All Widgets Design and Maintainer)
                                Author      Md. Minhaz
                                Email       mdm047767@gmail.com
                                Hire Me     https://pph.me/mdminhaz2003/
                                Repo Link   https://github.com/mdminhaz2003/XML-Modifier-GUI-by-Tkinter-Python
                                Location    Bangladesh
                                Date        04-08-2022 at 22:40:22 (GMT + 6)
===========================================================================================================
"""
from tkinter import Entry
from tkinter import Label
from tkinter import Button
from tkinter import Checkbutton
from tkinter.ttk import Combobox
from tkinter import StringVar
from tkinter import IntVar
from typing import Union
from functions import browse_file
from functions import dropdown_disabled
from functions import edit_text_validator


class Widgets(Entry, Label, Button):
    def __init__(self, master):
        super().__init__()

        self.master = master

    def label(
            self,
            text: str,
            row: int,
            column: int
    ) -> Union[Label, Label]:
        label = Label(master=self.master, text=text, background="gray20", foreground="orange", anchor="ne", width=35)
        label.grid(row=row, column=column)

        return label

    def edit_text(
            self,
            manager: dict,
            width: int = 50,
            show: str = None
    ):
        self.label(
            text=manager.get("field_name"),
            row=manager.get("row"),
            column=0
        )
        manager["variable"] = StringVar()

        if manager.get("number_of_input_field") == 1 and manager.get("is_file_selector"):
            edit_text = Entry(
                master=self.master,
                width=int(width + 8),
                show=show,
                background="#7883f0",
                borderwidth=0,
                fg="#050930",
                cursor="arrow",
                textvariable=manager.get("variable")
            )
            edit_text.grid(
                row=manager.get("row"),
                column=1,
                columnspan=2,
                padx=5,
                pady=5
            )
            edit_text.insert(index=0, string=f'Select your {manager.get("field_name")}')
            edit_text.bind(
                sequence='<Button-1>',
                func=lambda a=manager.get("placeholder"), b=manager.get("field_name"), c=manager.get('file_expression'), d=manager.get("file_path"):
                browse_file(
                    manager.get("variable"), a, b, c, str(d)
                )
            )
            return edit_text

        elif manager.get("number_of_input_field") == 1 and not manager.get("is_file_selector"):
            edit_text = Entry(
                master=self.master,
                width=int(width + 8),
                show=show,
                background="#fa1b2e",
                fg="#85e2ff",
                cursor="arrow",
                textvariable=manager.get("variable"),
                disabledbackground="#6e6e6e",
                disabledforeground="#bfc9ff",
                validate="focusout",
                validatecommand=lambda: edit_text_validator(
                    condition=manager.get("condition"),
                    variable=manager.get("variable"),
                    edit_text=edit_text,
                    err_msg=manager.get("error_msg")
                )
            )
            edit_text.grid(
                row=manager.get("row"),
                column=1,
                columnspan=2,
                pady=5
            )
            return edit_text

        elif manager.get("number_of_input_field") == 2 and not manager.get("is_dropdown"):
            manager["actual_value"] = StringVar()

            edit_text_actual = Entry(
                master=self.master,
                width=int(width / 2),
                show=show,
                cursor="none",
                borderwidth=0,
                background="gray20",
                textvariable=manager.get("actual_value"),
                disabledbackground="#6e6e6e",
                disabledforeground="#bfc9ff"
            )
            edit_text_new = Entry(
                master=self.master,
                width=int(width / 2 + 6),
                show=show,
                borderwidth=0,
                background="gray20",
                fg="#00eded",
                cursor="arrow",
                disabledbackground="#6e6e6e",
                disabledforeground="#bfc9ff",
                textvariable=manager.get("variable"),
                validate="focusout",
                validatecommand=lambda: edit_text_validator(
                    condition=manager.get("condition"),
                    variable=manager.get("variable"),
                    edit_text=edit_text_new,
                    err_msg=manager.get("error_msg")
                )
            )

            edit_text_actual.grid(row=manager.get("row"), column=1, columnspan=1, pady=5)
            edit_text_new.grid(row=manager.get("row"), column=2, columnspan=1, pady=5)
            return edit_text_actual, edit_text_new

        elif manager.get("number_of_input_field") == 2 and manager.get("is_dropdown"):
            manager["variable"].set(manager.get("options")[0])
            manager["actual_value"] = StringVar()

            edit_text_actual = Entry(
                master=self.master,
                width=int(width / 2),
                show=show,
                cursor="none",
                borderwidth=0,
                textvariable=manager.get("actual_value"),
                background="gray20",
                disabledbackground="#6e6e6e",
                disabledforeground="#bfc9ff"
            )

            dropdown = Combobox(
                master=self.master,
                textvariable=manager.get("variable"),
                background="green",
                values=manager.get("options"),
                width=int(width / 2 + 4),
                postcommand=lambda: dropdown_disabled(dropdown),
                cursor="arrow",
                foreground="black"
            )

            edit_text_actual.grid(row=manager.get("row"), column=1, columnspan=1, pady=5)
            dropdown.grid(row=manager.get("row"), column=2, columnspan=1, pady=5)

            return edit_text_actual, dropdown
        else:
            pass

    def button(
            self,
            btn_text: str,
            row: int,
            column: int,
            width: int = 10,
            command=None
    ) -> Union[Button, Button]:
        button = Button(
            master=self.master,
            text=btn_text,
            activebackground="#1f3fed",
            activeforeground="#1fed71",
            anchor="center",
            background="#1f3fed",
            command=command,
            compound="none",
            cursor="arrow",
            default="disabled",
            disabledforeground="#9da39f",
            foreground="#fcffff",
            height=1,
            width=width
        )
        button.grid(row=row, column=column, columnspan=1, pady=5)

        return button

    def check_button(
            self,
            check_btn_text: str,
            variable_name: IntVar,
            row: int,
            column: int,
            command=None
    ) -> Union[Checkbutton, Checkbutton]:
        check_btn = Checkbutton(
            master=self.master,
            selectcolor="gray",
            foreground="white",
            background="#1f3fed",
            text=check_btn_text,
            activeforeground="yellow",
            activebackground="blue",
            command=command,
            variable=variable_name
        )
        check_btn.grid(row=row, column=column, columnspan=2)
        return check_btn
