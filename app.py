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
from functions import check_button_function


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

        self.time_format_matcher = re.compile(r'([0-2])([0-9]):([0-5])([0-9]):([0-5])([0-9])$')
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
            command=lambda: check_button_function(
                self.to_departure_location_check_btn_status,
                self.app["arrival_location_longitude"][1],
                self.app["arrival_location_latitude"][1]
            )
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
                    self.exist_data_input()
                else:
                    err_message_dialog(extra=True, custom_msg="Please Select Correct XML File.")

            except Exception as e:
                err_message_dialog(extra=True, custom_msg="Please Select Correct XML File.")
                print(e)
        else:
            err_message_dialog(extra=True, custom_msg="Select your valid XML file from file store.")

    def exist_data_input(self):
        all_data_except_settings = [
            {"key": "request_id", "value": self.request_id},
            {
                "key": "service_and_vehicle_hours_start",
                "value": re.search(self.time_format_matcher, self.vehicle_hours_start_datetime).group()
            },
            {
                "key": "service_and_vehicle_hours_end",
                "value": re.search(self.time_format_matcher, self.vehicle_hours_end_datetime).group()
            },
            {
                "key": "service_time",
                "value": re.search(r'[0-9]+', self.first_service.find(f'./{self.xml_ns}Duration').text).group()
            },
            {
                "key": "departure_location_longitude",
                "value": self.first_vehicle.find(f'./{self.xml_ns}Location/{self.xml_ns}Coord').get("x")
            },
            {
                "key": "departure_location_latitude",
                "value": self.first_vehicle.find(f'./{self.xml_ns}Location/{self.xml_ns}Coord').get("y")
            },
            {
                "key": "arrival_location_longitude",
                "value": self.first_vehicle.find(f'./{self.xml_ns}EndLocation/{self.xml_ns}Coord').get("x")
            },
            {
                "key": "arrival_location_latitude",
                "value": self.first_vehicle.find(f'./{self.xml_ns}EndLocation/{self.xml_ns}Coord').get("y")
            },
            {
                "key": "vehicle_autonomy",
                "value": self.first_vehicle.find(f'./{self.xml_ns}MaxDailyKM').text
            },
            {
                "key": "vehicle_cost_driver_daily_fixed",
                "value": self.first_vehicle.find(f'./{self.xml_ns}CostFixed').text
            },
            {
                "key": "vehicle_cost_driver_per_km",
                "value": self.first_vehicle.find(f'./{self.xml_ns}CostKm').text
            },
            {
                "key": "vehicle_cost_driver_hourly",
                "value": self.first_vehicle.find(f'./{self.xml_ns}CostHour').text
            },
            {
                "key": "vehicle_cost_driver_overtime",
                "value": self.first_vehicle.find(f'./{self.xml_ns}CostOvertime').text
            },
            {
                "key": "vehicle_capacity_parameters_units",
                "value": self.first_vehicle.find(f'./{self.xml_ns}CapacityUnits').text
            },
            {
                "key": "vehicle_capacity_parameters_payloads",
                "value": self.first_vehicle.find(f'./{self.xml_ns}CapacityKg').text
            },
            {
                "key": "vehicle_capacity_parameters_volume",
                "value": self.first_vehicle.find(f'./{self.xml_ns}CapacityM3').text
            }
        ]

        for item in all_data_except_settings:
            self.data_input_helper(key=item.get("key"), data=item.get("value"))

        for parameter in self.settings.iter(f"{self.xml_ns}Parameter"):
            param_name = parameter.find(f"{self.xml_ns}Name").text

            if param_name == "Priority":
                self.data_input_helper("priority_weight", parameter.find(f'./{self.xml_ns}Weight').text)
                self.data_input_helper("priority_factor", parameter.find(f'./{self.xml_ns}Factor').text)
            elif param_name == "Cost":
                self.data_input_helper("cost_weight", parameter.find(f'./{self.xml_ns}Weight').text)
                self.data_input_helper("cost_factor", parameter.find(f'./{self.xml_ns}Factor').text)
            elif param_name == "Delay":
                self.data_input_helper("delay_mandatory", parameter.find(f'./{self.xml_ns}Mandatory').text)
                self.data_input_helper("delay_weight", parameter.find(f'./{self.xml_ns}Weight').text)
                self.data_input_helper("delay_factor", parameter.find(f'./{self.xml_ns}Factor').text)
            elif param_name == "AvoidOvertime":
                self.data_input_helper("avoid_overtime", parameter.find(f'./{self.xml_ns}Value').text)
            elif param_name == "AvoidExtraDriving":
                self.data_input_helper("avoid_extra_driving", parameter.find(f'./{self.xml_ns}Value').text)
            elif param_name == "Allocate":
                self.data_input_helper("allocate_mandatory", parameter.find(f'./{self.xml_ns}Mandatory').text)
                self.data_input_helper("allocate_weight", parameter.find(f'./{self.xml_ns}Weight').text)
                self.data_input_helper("allocate_factor", parameter.find(f'./{self.xml_ns}Factor').text)
            elif param_name == "Iterations":
                self.data_input_helper("iterations", parameter.find(f'./{self.xml_ns}Value').text)
            elif param_name == "RouteWeight":
                self.data_input_helper("route_weight", parameter.find(f'./{self.xml_ns}Value').text)
            elif param_name == "MaxServiceDelay":
                self.data_input_helper("max_service_delay", parameter.find(f'./{self.xml_ns}Value').text)
            elif param_name == "MaxDiffAllocate":
                self.data_input_helper("max_diff_allocate", parameter.find(f'./{self.xml_ns}Value').text)
            elif param_name == "OvertimeUnits":
                self.data_input_helper("overtime_units", parameter.find(f'./{self.xml_ns}Value').text)
            elif param_name == "LimitOvertimeBefore":
                self.data_input_helper("limit_overtime_before", parameter.find(f'./{self.xml_ns}Value').text)
            elif param_name == "LimitOvertimeAfter":
                self.data_input_helper("limit_overtime_after", parameter.find(f'./{self.xml_ns}Value').text)
            elif param_name == "MinHoursBreak":
                self.data_input_helper("min_hours_break", parameter.find(f'./{self.xml_ns}Value').text)
            elif param_name == "AllocateMode":
                self.data_input_helper("allocate_mode", parameter.find(f'./{self.xml_ns}Value').text)
            elif param_name == "GroupServices":
                self.data_input_helper("group_service_mandatory", parameter.find(f'./{self.xml_ns}Mandatory').text)
                self.data_input_helper("group_service_weight", parameter.find(f'./{self.xml_ns}Weight').text)
                self.data_input_helper("group_service_factor", parameter.find(f'./{self.xml_ns}Factor').text)
            elif param_name == "GroupServicesMaxMeters":
                self.data_input_helper("group_service_max_meter", parameter.find(f'./{self.xml_ns}Value').text)
            elif param_name == "RestrictToServiceWindow":
                self.data_input_helper("restrict_service_window", parameter.find(f'./{self.xml_ns}Value').text)
            elif param_name == "TimeFactor":
                self.data_input_helper("time_factor", parameter.find(f'./{self.xml_ns}Value').text)
            elif param_name == "AllVehicles":
                self.data_input_helper("all_vehicles", parameter.find(f'./{self.xml_ns}Value').text)
            else:
                pass

    def data_input_helper(self, key: str, data: str):
        if widgets_info.get(key)["number_of_input_field"] == 1:
            clear_edit_text(text_variable=widgets_info.get(key)["variable"])
            widgets_info.get(key)["variable"].set(data)
            set_config(
                field_name=self.app.get(key),
                config="disabled"
            )
        elif widgets_info.get(key)["number_of_input_field"] == 2 and widgets_info.get(key)["is_dropdown"]:
            clear_edit_text(text_variable=widgets_info.get(key)["actual_value"])
            widgets_info.get(key)["actual_value"].set(data)
            set_config(
                field_name=self.app.get(key)[0],
                config="disabled"
            )
        elif widgets_info.get(key)["number_of_input_field"] == 2 and not widgets_info.get(key)["is_dropdown"]:
            clear_edit_text(text_variable=widgets_info.get(key)["actual_value"])
            clear_edit_text(text_variable=widgets_info.get(key)["variable"])
            widgets_info.get(key)["actual_value"].set(data)
            set_config(
                field_name=self.app.get(key)[0],
                config="disabled"
            )
        else:
            pass
