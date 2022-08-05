"""
===========================================================================================================
                                File        app.py (Entry point)
                                Author      Md. Minhaz
                                Email       mdm047767@gmail.com
                                Hire Me     https://pph.me/mdminhaz2003/
                                Repo Link   https://github.com/mdminhaz2003/XML-Modifier-GUI-by-Tkinter-Python
                                Location    Bangladesh
                                Date        04-08-2022 at 22:40:58 (GMT + 6)
===========================================================================================================
"""
import re
import os
from widgets_info import widgets_info
from widgets import Widgets
from tkinter import IntVar
from functions import set_config
from functions import err_message_dialog
from xml.etree import ElementTree
from functions import clear_edit_text


class Ui:
    def __init__(self, master: Widgets = None):
        self.master = master

        self.to_departure_location_check_btn = None
        self.to_departure_location_check_btn_status = IntVar()
        self.to_departure_location_check_btn_status.set(1)

        self.read_files_btn = None
        self.submit_btn = None

        self.app = {}

        self.xml_tree = None
        self.xml_root = None

        self.xml_ns = r'{https://lastmile.team}'
        self.request = None
        self.request_id = None
        self.first_vehicle = None
        self.first_service = None
        self.settings = None

        self.vehicle_hours_start_datetime = None
        self.vehicle_hours_end_datetime = None

    def edit_text_packer(self) -> None:
        for key, value in zip(widgets_info.keys(), widgets_info.values()):
            if value.get("no_need_pack") is None:
                self.app[key] = self.master.edit_text(manager=value)

        self.to_departure_location_check_btn = self.master.check_button(
            check_btn_text="Do Vehicles arrive to departure location",
            variable_name=self.to_departure_location_check_btn_status,
            row=10,
            column=1,
            command=None
        )

        set_config(
            field_name=self.app["arrival_location_longitude"][1],
            config="disabled"
        )
        set_config(
            field_name=self.app["arrival_location_latitude"][1],
            config="disabled"
        )

        self.read_files_btn = self.master.button(
            btn_text="Read Files",
            row=2,
            column=2,
            command=self.read_xml
        )
        self.submit_btn = self.master.button(
            btn_text="Submit",
            row=49,
            column=1,
            command=None
        )

    def read_xml(self):
        if os.path.exists(widgets_info.get("xml_file_path")["variable"].get()):
            try:
                self.xml_tree = ElementTree.parse(widgets_info.get("xml_file_path")["variable"].get())
                self.xml_root = self.xml_tree.getroot()

                # Exist Data Input
                if self.xml_root.tag.lower() == f"{self.xml_ns}requests":
                    self.request = self.xml_root.find(f"./{self.xml_ns}Request")
                    self.request_id = self.request.get("requestid")
                    self.first_vehicle = self.xml_root.find(f'.//{self.xml_ns}Vehicles/{self.xml_ns}Vehicle')
                    self.first_service = self.xml_root.find(f'.//{self.xml_ns}Services/{self.xml_ns}Service')
                    self.settings = self.xml_root.find(f'.//{self.xml_ns}Settings')

                    self.vehicle_hours_start_datetime = self.first_vehicle.find(f'./{self.xml_ns}StartTimeWorkday').text
                    self.vehicle_hours_end_datetime = self.first_vehicle.find(f'./{self.xml_ns}EndTimeWorkday').text
                    # self.exist_data_input()
                else:
                    err_message_dialog(extra=True, custom_msg="Please Select Correct XML File.")

            except Exception as e:
                err_message_dialog(extra=True, custom_msg="Please Select Correct XML File.")
                print(e)
        else:
            err_message_dialog(extra=True, custom_msg="Select your valid XML file from file store.")
