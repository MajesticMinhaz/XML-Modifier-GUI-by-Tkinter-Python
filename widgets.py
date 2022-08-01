from tkinter import Entry
from tkinter import Label
from tkinter import Button
from tkinter import Checkbutton
from tkinter import RIGHT
from tkinter.ttk import Combobox
from tkinter import StringVar
from tkinter import IntVar
from typing import Union
from functions import browse_file
from functions import dropdown_disabled


class Widgets(Entry, Label, Button):
    def __init__(self, master):
        super().__init__()

        self.master = master

    def label(
            self,
            label_text: str,
            row: int,
            column: int
    ) -> Union[Label, Label]:
        label = Label(
            master=self.master,
            text=label_text,
            foreground="#050930",
            justify=RIGHT,
            anchor="ne",
            width=30
        )
        label.grid(
            row=row,
            column=column
        )

        return label

    def edit_text(
            self,
            section_name: str,
            row: int,
            width: int = 60,
            show=None,
            number_of_input_box: int = 1,
            file_selector: bool = False,
            select_file_expression: str = None,
            base_path: bool = False,
            need_dropdown: bool = False,
            dropdown_variable_name: StringVar = None,
            dropdown_options: list = None
    ):
        self.label(
            label_text=section_name,
            row=row,
            column=0
        )

        if number_of_input_box == 1 and file_selector:
            edit_text = Entry(
                master=self.master,
                width=int(width + 7),
                show=show,
                background="#7883f0",
                fg="#050930",
                cursor="arrow"
            )
            edit_text.grid(
                row=row,
                column=1,
                columnspan=2,
                padx=5
            )
            edit_text.insert(
                index=0,
                string=f'Select your {section_name}'
            )
            edit_text.bind(
                sequence='<Button-1>',
                func=lambda a=f"Select your {section_name}", b=section_name, c=select_file_expression, d=base_path:
                browse_file(
                    edit_text, a, b, c, str(d)
                )
            )
            return edit_text
        elif number_of_input_box == 1 and not file_selector:
            edit_text = Entry(
                master=self.master,
                width=int(width + 7),
                show=show,
                background="#fa1b2e",
                fg="#85e2ff",
                cursor="arrow"
            )
            edit_text.grid(
                row=row,
                column=1,
                columnspan=2
            )
            return edit_text
        elif number_of_input_box == 2 and not need_dropdown:
            edit_text_actual = Entry(
                master=self.master,
                width=int(width / 2),
                show=show,
                cursor="none",
                borderwidth=0,
                background="#6e6e6e",
                disabledbackground="#6e6e6e",
                disabledforeground="#bfc9ff"
            )
            edit_text_actual.insert(0, "Hi")
            edit_text_actual.configure(state="disabled")
            edit_text_new = Entry(
                master=self.master,
                width=int(width / 2 + 6),
                show=show,
                background="#438f00",
                fg="#00eded",
                cursor="arrow"
            )

            edit_text_actual.grid(
                row=row,
                column=1,
                columnspan=1,
                padx=5
            )
            edit_text_new.grid(
                row=row,
                column=2,
                columnspan=1
            )

            return edit_text_actual, edit_text_new
        elif number_of_input_box == 2 and need_dropdown:
            dropdown_variable_name.set(dropdown_options[0])

            edit_text_actual = Entry(
                master=self.master,
                width=int(width / 2),
                show=show,
                cursor="none",
                borderwidth=0,
                background="#6e6e6e",
                disabledbackground="#6e6e6e",
                disabledforeground="#bfc9ff"
            )
            dropdown_variable_name.set(dropdown_options[0])
            dropdown = Combobox(
                master=self.master,
                textvariable=dropdown_variable_name,
                background="green",
                values=dropdown_options,
                width=int(width / 2 + 4),
                postcommand=lambda: dropdown_disabled(dropdown),
                cursor="arrow",
                foreground="blue"
            )

            edit_text_actual.grid(
                row=row,
                column=1,
                columnspan=1
            )

            dropdown.grid(
                row=row,
                column=2,
                columnspan=1
            )

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
        button.grid(
            row=row,
            column=column,
            columnspan=1
        )
        return button

    def check_button(
            self,
            check_btn_text: str,
            variable_name: IntVar,
            row: int,
            column: int,
            command=lambda: None
    ) -> Union[Checkbutton, Checkbutton]:
        check_btn = Checkbutton(
            master=self.master,
            selectcolor="gray",
            foreground="white",
            background="#1f3fed",
            text=check_btn_text,
            activeforeground="yellow",
            activebackground="blue"
        )
        check_btn.grid(
            row=row,
            column=column,
            columnspan=1
        )
        return check_btn
