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
import json
import re
import os
import shutil
from datetime import timedelta
from widgets_info import widgets_info
from widgets import Widgets
from tkinter import IntVar
from functions import set_config
from functions import err_message_dialog
from xml.etree import ElementTree
from functions import clear_edit_text
from functions import check_button_function
from functions import is_empty
from tkinter import messagebox


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
        self.lmt_json_data = None

        self.time_format = re.compile(r'([0-1][0-9]|(2[0-3])):([0-5][0-9]):([0-5][0-9])$')
        self.vehicle_hours_start_datetime = None
        self.vehicle_hours_end_datetime = None

        self.new_request_id = None

    def widget_packer(self) -> None:
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
            command=self.submit_btn_handler
        )

    def read_xml(self):
        if os.path.exists(widgets_info.get("xml_file_path")["variable"].get()):
            try:
                self.xml_tree = ElementTree.parse(widgets_info.get("xml_file_path")["variable"].get())
                self.xml_root = self.xml_tree.getroot()

                lmt_input_copert_path = os.path.join(
                    re.search(
                        pattern=r"^.*([0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]_.*/)",
                        string=widgets_info.get("xml_file_path")["variable"].get()
                    ).group()[0:-9],
                    "lmt_LEAD_input_to_COPERT.json"
                )
                lmt_input_evco2_path = os.path.join(
                    re.search(
                        pattern=r"^.*([0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]_.*/)",
                        string=widgets_info.get("xml_file_path")["variable"].get()
                    ).group()[0:-9],
                    "lmt_LEAD_input_to_EVCO2.json"
                )

                if os.path.exists(lmt_input_evco2_path):
                    with open(lmt_input_evco2_path, "r") as read_json:
                        self.lmt_json_data = read_json.read()
                        self.lmt_json_data = json.loads(self.lmt_json_data)[0]
                        read_json.close()
                if os.path.exists(lmt_input_copert_path):
                    with open(lmt_input_copert_path, "r") as read_json:
                        self.lmt_json_data = read_json.read()
                        self.lmt_json_data = json.loads(self.lmt_json_data)[0]
                        read_json.close()
                else:
                    pass

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
                "value": re.search(self.time_format, self.vehicle_hours_start_datetime).group()
            },
            {
                "key": "service_and_vehicle_hours_end",
                "value": re.search(self.time_format, self.vehicle_hours_end_datetime).group()
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

    def submit_btn_handler(self) -> None:
        check_btn_status = self.to_departure_location_check_btn_status.get()

        # Checking Fields
        if is_empty(widgets_info.get("twin_iteration_n")["variable"]):
            err_message_dialog(field_name=widgets_info.get("twin_iteration_n")["field_name"])
        elif check_btn_status.__eq__(0) and is_empty(widgets_info.get("arrival_location_longitude")["variable"]):
            err_message_dialog(field_name=widgets_info.get("arrival_location_longitude")["field_name"])
        elif check_btn_status.__eq__(0) and is_empty(widgets_info.get("arrival_location_latitude")["variable"]):
            err_message_dialog(field_name=widgets_info.get("arrival_location_latitude")["field_name"])
        else:
            self.new_request_id = f'{self.request_id}-{widgets_info.get("twin_iteration_n")["variable"].get()}'
            self.update_xml()

    def update_xml(self):
        ElementTree.register_namespace('', "https://lastmile.team")
        ElementTree.register_namespace('xsd', "http://www.w3.org/2001/XMLSchema")
        ElementTree.register_namespace('xsi', "http://www.w3.org/2001/XMLSchema-instance")

        self.xml_root.find(f'./{self.xml_ns}Request').set('requestid', self.new_request_id)

        if not is_empty(text_variable=widgets_info.get("service_and_vehicle_hours_start")["variable"]):
            if re.fullmatch(self.time_format, widgets_info["service_and_vehicle_hours_start"]["variable"].get()):
                new_start_time = widgets_info["service_and_vehicle_hours_start"]["variable"].get()
                start_time = timedelta(
                    hours=float(new_start_time[0:2]),
                    minutes=float(new_start_time[3:5]),
                    seconds=float(new_start_time[6:])
                )

                if is_empty(text_variable=widgets_info.get('service_and_vehicle_hours_end')['variable']):
                    end_time = timedelta(
                        hours=float(self.vehicle_hours_end_datetime[-8:-6]),
                        minutes=float(self.vehicle_hours_end_datetime[-5:-3]),
                        seconds=float(self.vehicle_hours_end_datetime[-2:])
                    )

                else:
                    new_end_time = widgets_info["service_and_vehicle_hours_end"]["variable"].get()
                    end_time = timedelta(
                        hours=float(new_end_time[0:2]),
                        minutes=float(new_end_time[3:5]),
                        seconds=float(new_end_time[6:])
                    )

                if end_time.__sub__(start_time).total_seconds() > 0:
                    for start_time_workday in self.xml_root.iter(f'{self.xml_ns}StartTimeWorkday'):
                        start_time_workday.text = re.sub(
                            pattern=self.time_format,
                            repl=widgets_info["service_and_vehicle_hours_start"]["variable"].get(),
                            string=self.vehicle_hours_start_datetime
                        )

                    for window_start in self.xml_root.iter(f'{self.xml_ns}Window'):
                        window_start.set(
                            'start',
                            re.sub(
                                pattern=self.time_format,
                                repl=widgets_info["service_and_vehicle_hours_start"]["variable"].get(),
                                string=self.vehicle_hours_start_datetime
                            )
                        )
                else:
                    messagebox.showerror("Wrong Value", "End Time is less then Start time.")
            else:
                messagebox.showerror("Wrong Value", "I found wrong value in Vehicle Hours Start Field. That's why I "
                                                    "am skipped this part")

        if not is_empty(text_variable=widgets_info["service_and_vehicle_hours_end"]["variable"]):
            if re.fullmatch(self.time_format, widgets_info["service_and_vehicle_hours_end"]["variable"].get()):
                new_end_time = widgets_info["service_and_vehicle_hours_end"]["variable"].get()
                end_time = timedelta(
                    hours=float(new_end_time[0:2]),
                    minutes=float(new_end_time[3:5]),
                    seconds=float(new_end_time[6:])
                )

                if is_empty(text_variable=widgets_info["service_and_vehicle_hours_end"]["variable"]):
                    start_time = timedelta(
                        hours=float(self.vehicle_hours_start_datetime[-8:-6]),
                        minutes=float(self.vehicle_hours_start_datetime[-5:-3]),
                        seconds=float(self.vehicle_hours_start_datetime[-2:])
                    )

                else:
                    new_start_time = widgets_info["service_and_vehicle_hours_start"]["variable"].get()
                    start_time = timedelta(
                        hours=float(new_start_time[0:2]),
                        minutes=float(new_start_time[3:5]),
                        seconds=float(new_start_time[6:])
                    )

                if end_time.__sub__(start_time).total_seconds() > 0:
                    for end_time_workday in self.xml_root.iter(f'{self.xml_ns}EndTimeWorkday'):
                        end_time_workday.text = re.sub(
                            pattern=self.time_format,
                            repl=widgets_info["service_and_vehicle_hours_end"]["variable"].get(),
                            string=self.vehicle_hours_end_datetime
                        )

                    for window_end in self.xml_root.iter(f'{self.xml_ns}Window'):
                        window_end.set(
                            'end',
                            re.sub(
                                pattern=self.time_format,
                                repl=widgets_info["service_and_vehicle_hours_end"]["variable"].get(),
                                string=self.vehicle_hours_end_datetime
                            )
                        )
                else:
                    messagebox.showerror("Wrong Value", "End Time is less then Start time.")
            else:
                messagebox.showerror("Wrong Value", "I found wrong value in Vehicle Hours Start Field. That's why I "
                                                    "am skipped this part")

        if not is_empty(widgets_info["service_time"]["variable"]):
            for duration in self.xml_root.iter(f'{self.xml_ns}Duration'):
                duration.text = re.sub(
                    pattern=r'[0-9]+',
                    repl=widgets_info["service_time"]["variable"].get(),
                    string=duration.text
                )

        if not is_empty(text_variable=widgets_info['departure_location_longitude']["variable"]):
            for vehicle in self.xml_root.iter(f'{self.xml_ns}Vehicle'):
                vehicle.find(f'./{self.xml_ns}Location/{self.xml_ns}Coord').set(
                    'x', widgets_info['departure_location_longitude']["variable"].get()
                )

        if not is_empty(text_variable=widgets_info['departure_location_latitude']["variable"]):
            for vehicle in self.xml_root.iter(f'{self.xml_ns}Vehicle'):
                vehicle.find(f'./{self.xml_ns}Location/{self.xml_ns}Coord').set(
                    'y', widgets_info['departure_location_latitude']["variable"].get()
                )

        if not is_empty(text_variable=widgets_info["arrival_location_longitude"]["variable"]):
            for vehicle in self.xml_root.iter(f'{self.xml_ns}Vehicle'):
                vehicle.find(f'./{self.xml_ns}EndLocation/{self.xml_ns}Coord').set(
                    'x', widgets_info["arrival_location_longitude"]["variable"].get()
                )

        if not is_empty(text_variable=widgets_info["arrival_location_latitude"]["variable"]):
            for vehicle in self.xml_root.iter(f'{self.xml_ns}Vehicle'):
                vehicle.find(f'./{self.xml_ns}EndLocation/{self.xml_ns}Coord').set(
                    'y', widgets_info["arrival_location_latitude"]["variable"].get()
                )

        if self.to_departure_location_check_btn_status.get().__eq__(0):
            for return_base in self.xml_root.iter(f'{self.xml_ns}ReturnBase'):
                return_base.text = 'N'

        if self.to_departure_location_check_btn_status.get().__eq__(1):
            for return_base in self.xml_root.iter(f'{self.xml_ns}ReturnBase'):
                return_base.text = 'Y'

        if not is_empty(text_variable=widgets_info["vehicle_autonomy"]["variable"]):
            for max_daily_km in self.xml_root.iter(f'{self.xml_ns}MaxDailyKM'):
                max_daily_km.text = widgets_info["vehicle_autonomy"]["variable"].get()

        if not is_empty(text_variable=widgets_info['vehicle_cost_driver_daily_fixed']["variable"]):
            for cost_fixed in self.xml_root.iter(f'{self.xml_ns}CostFixed'):
                cost_fixed.text = widgets_info['vehicle_cost_driver_daily_fixed']["variable"].get()

        if not is_empty(text_variable=widgets_info['vehicle_cost_driver_per_km']["variable"]):
            for cost_km in self.xml_root.iter(f'{self.xml_ns}CostKm'):
                cost_km.text = widgets_info['vehicle_cost_driver_per_km']["variable"].get()

        if not is_empty(text_variable=widgets_info['vehicle_cost_driver_hourly']["variable"]):
            for cost_hour in self.xml_root.iter(f'{self.xml_ns}CostHour'):
                cost_hour.text = widgets_info['vehicle_cost_driver_hourly']["variable"].get()

        if not is_empty(text_variable=widgets_info['vehicle_cost_driver_overtime']["variable"]):
            for cost_overtime in self.xml_root.iter(f'{self.xml_ns}CostOvertime'):
                cost_overtime.text = widgets_info['vehicle_cost_driver_overtime']["variable"].get()

        if not is_empty(text_variable=widgets_info['vehicle_capacity_parameters_units']["variable"]):
            for capacity_units in self.xml_root.iter(f'{self.xml_ns}CapacityUnits'):
                capacity_units.text = widgets_info['vehicle_capacity_parameters_units']["variable"].get()

        if not is_empty(text_variable=widgets_info['vehicle_capacity_parameters_payloads']["variable"]):
            for capacity_payloads in self.xml_root.iter(f'{self.xml_ns}CapacityKg'):
                capacity_payloads.text = widgets_info['vehicle_capacity_parameters_payloads']["variable"].get()

        if not is_empty(text_variable=widgets_info['vehicle_capacity_parameters_volume']["variable"]):
            for capacity_volume in self.xml_root.iter(f'{self.xml_ns}CapacityM3'):
                capacity_volume.text = widgets_info['vehicle_capacity_parameters_volume']["variable"].get()

        for parameter in self.xml_root.iter(f"{self.xml_ns}Parameter"):
            param_name = parameter.find(f'{self.xml_ns}Name').text
            if param_name == "Priority":
                if not is_empty(text_variable=widgets_info["priority_weight"]["variable"]):
                    parameter.find(f'./{self.xml_ns}Weight').text = widgets_info["priority_weight"]["variable"].get()
                if not is_empty(text_variable=widgets_info["priority_factor"]["variable"]):
                    parameter.find(f'./{self.xml_ns}Factor').text = widgets_info["priority_factor"]["variable"].get()

            elif param_name == "Cost":
                if not is_empty(text_variable=widgets_info["cost_weight"]["variable"]):
                    parameter.find(f'./{self.xml_ns}Weight').text = widgets_info["cost_weight"]["variable"].get()
                if not is_empty(text_variable=widgets_info["cost_factor"]["variable"]):
                    parameter.find(f'./{self.xml_ns}Factor').text = widgets_info["cost_factor"]["variable"].get()

            elif param_name == "Delay":
                parameter.find(f'./{self.xml_ns}Mandatory').text = widgets_info["delay_mandatory"]["variable"].get()
                if not is_empty(text_variable=widgets_info["delay_weight"]["variable"]):
                    parameter.find(f'./{self.xml_ns}Weight').text = widgets_info["delay_weight"]["variable"].get()
                if not is_empty(text_variable=widgets_info["delay_factor"]["variable"]):
                    parameter.find(f'./{self.xml_ns}Factor').text = widgets_info["delay_factor"]["variable"].get()

            elif param_name == "AvoidOvertime":
                parameter.find(f'./{self.xml_ns}Value').text = widgets_info["avoid_overtime"]["variable"].get()

            elif param_name == "AvoidExtraDriving":
                parameter.find(f'./{self.xml_ns}Value').text = widgets_info["avoid_extra_driving"]["variable"].get()

            elif param_name == "Allocate":
                parameter.find(f'./{self.xml_ns}Mandatory').text = widgets_info["allocate_mandatory"]["variable"].get()

                if not is_empty(text_variable=widgets_info["allocate_weight"]["variable"]):
                    parameter.find(f'./{self.xml_ns}Weight').text = widgets_info["allocate_weight"]["variable"].get()
                if not is_empty(text_variable=widgets_info["allocate_factor"]["variable"]):
                    parameter.find(f'./{self.xml_ns}Factor').text = widgets_info["allocate_factor"]["variable"].get()

            elif param_name == "Iterations":
                if not is_empty(text_variable=widgets_info["iterations"]["variable"]):
                    parameter.find(f'./{self.xml_ns}Value').text = widgets_info["iterations"]["variable"].get()

            elif param_name == "RouteWeight":
                parameter.find(f'./{self.xml_ns}Value').text = widgets_info["route_weight"]["variable"].get()

            elif param_name == "MaxServiceDelay":
                if not is_empty(text_variable=widgets_info["max_service_delay"]["variable"]):
                    parameter.find(f'./{self.xml_ns}Value').text = widgets_info["max_service_delay"]["variable"].get()

            elif param_name == "MaxDiffAllocate":
                if not is_empty(text_variable=widgets_info["max_diff_allocate"]["variable"]):
                    parameter.find(f'./{self.xml_ns}Value').text = widgets_info["max_diff_allocate"]["variable"].get()

            elif param_name == "OvertimeUnits":
                if not is_empty(text_variable=widgets_info["overtime_units"]["variable"]):
                    parameter.find(f'./{self.xml_ns}Value').text = widgets_info["overtime_units"]["variable"].get()

            elif param_name == "LimitOvertimeBefore":
                if not is_empty(text_variable=widgets_info["limit_overtime_before"]["variable"]):
                    parameter.find(f'./{self.xml_ns}Value').text = widgets_info["limit_overtime_before"]["variable"].get()

            elif param_name == "LimitOvertimeAfter":
                if not is_empty(text_variable=widgets_info["limit_overtime_after"]["variable"]):
                    parameter.find(f'./{self.xml_ns}Value').text = widgets_info["limit_overtime_after"]["variable"].get()

            elif param_name == "MinHoursBreak":
                if not is_empty(text_variable=widgets_info["min_hours_break"]["variable"]):
                    parameter.find(f'./{self.xml_ns}Value').text = widgets_info["min_hours_break"]["variable"].get()

            elif param_name == "AllocateMode":
                parameter.find(f'./{self.xml_ns}Value').text = widgets_info["allocate_mode"]["variable"].get()

            elif param_name == "GroupServices":
                parameter.find(f'./{self.xml_ns}Mandatory').text = widgets_info["group_service_mandatory"]["variable"].get()

                if not is_empty(text_variable=widgets_info["group_service_weight"]["variable"]):
                    parameter.find(f'./{self.xml_ns}Weight').text = widgets_info["group_service_weight"]["variable"].get()
                if not is_empty(text_variable=widgets_info["group_service_factor"]["variable"]):
                    parameter.find(f'./{self.xml_ns}Factor').text = widgets_info["group_service_factor"]["variable"].get()

            elif param_name == "GroupServicesMaxMeters":
                if not is_empty(text_variable=widgets_info["group_service_max_meter"]["variable"]):
                    parameter.find(f'./{self.xml_ns}Value').text = widgets_info["group_service_max_meter"]["variable"].get()

            elif param_name == "RestrictToServiceWindow":
                parameter.find(f'./{self.xml_ns}Value').text = widgets_info["restrict_service_window"]["variable"].get()

            elif param_name == "TimeFactor":
                if not is_empty(text_variable=widgets_info["time_factor"]["variable"]):
                    parameter.find(f'./{self.xml_ns}Value').text = widgets_info["time_factor"]["variable"].get()

            elif param_name == "AllVehicles":
                parameter.find(f'./{self.xml_ns}Value').text = widgets_info["all_vehicles"]["variable"].get()

            else:
                pass

        self.create_folders()

    def create_folders(self):
        if not is_empty(text_variable=widgets_info.get('base_path')['variable']):
            if '_templates' in os.listdir(widgets_info.get("base_path")["variable"].get()):
                base_folder = f"{widgets_info.get('base_path')['variable'].get()}-output"
                sub_folder = f'YYYYMMDD_LL1_{widgets_info.get("twin_iteration_n")["variable"].get()}'
                for directory_name in os.listdir(widgets_info.get("base_path")["variable"].get()):
                    if re.fullmatch(pattern=r"^[0-9]+_LL1_baseline$", string=directory_name):
                        sub_folder = re.sub(
                            pattern=r"(baseline)$",
                            repl=widgets_info.get("twin_iteration_n")["variable"].get(),
                            string=directory_name
                        )
                    else:
                        pass
                sub_folder = os.path.join(base_folder, sub_folder)
                request_folder = os.path.join(sub_folder, "Request")
                new_xml_file_path = os.path.join(request_folder, f'{self.new_request_id}.xml')

                try:
                    os.mkdir(base_folder)
                    os.mkdir(sub_folder)
                    os.mkdir(request_folder)
                except FileExistsError:
                    shutil.rmtree(base_folder)
                    os.mkdir(base_folder)
                    os.mkdir(sub_folder)
                    os.mkdir(request_folder)
                except OSError:
                    shutil.rmtree(base_folder)
                    os.mkdir(base_folder)
                    os.mkdir(sub_folder)
                    os.mkdir(request_folder)
                self.xml_tree.write(new_xml_file_path, xml_declaration=True)

                source_directory = os.path.join(widgets_info.get('base_path')['variable'].get(), "_templates")

                for file_name in os.listdir(source_directory):
                    if file_name == "COPERT_vehicle_types.xlsx":
                        continue
                    else:
                        source = os.path.join(source_directory, file_name)
                        destination = os.path.join(sub_folder, file_name)

                        if os.path.isfile(source):
                            shutil.copy(source, destination)
                        else:
                            pass

                messagebox.showinfo(title="Successful", message=f"Successfully created {new_xml_file_path}.")
            else:
                messagebox.showerror("Wrong Directory", "You have selected a wrong directory as Base Path.")
        else:
            err_message_dialog(field_name="Base Path")
