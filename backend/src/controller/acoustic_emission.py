from datetime import datetime

import socket
import json

class AcousticEmissionController:

    def __init__(self, ip_address: str, port: int, output_dir: str):
        self.ip_address = ip_address
        self.port = port
        self.output_dir = output_dir
        self.client_socket = None

    def get_sensors(self) -> list[str]:
        params = {
            "verbosity": "all",
        }
        response_string = self.__call("GetSensors", params=params)
        response_dict = json.loads(response_string)
        return response_dict["result"]["sensors"]

    def is_alive(self) -> bool:
        response_string = self.__call("GetSystemStatus")
        response_dict = json.loads(response_string)
        return response_dict["result"]["bunits_ae"]["alive"] > 0


    def get_time(self) -> int:
        response_string = self.__call("GetSystemTime")
        response_dict = json.loads(response_string)
        return response_dict["result"]["gtime"]

    def configure(self, config: str):
        params = {
            "config": config,
            "verbosity": "all",
        }
        return self.__call("Configure", params=params)

    def start_recording(self, measurement_name: str, record_history_secs: int):
        params = {
            "measurement_name": measurement_name,
            "record_history_secs": record_history_secs,
            "path": self.output_dir # if this is not supported, set measurement_name to desired output filename with absolute path
        }
        self.__call("StartRecording", params=params)

    def pause_recording(self):
        self.__call("PauseRecording")

    def stop_recording(self):
        self.__call("StopRecording")
        
    def get_recording_state(self) -> str:
        response_string = self.__call("GetRecordingState")
        response_dict = json.loads(response_string)
        return response_dict["result"]["recording_mode_text"]

    def __enter__(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.ip_address, self.port))
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.client_socket.close()
        pass

    def __call(self, method, id = 1, params = {}):
        call_values = {
            'jsonrpc': '2.0', 
            'method': method, 
            'id': id,
            "params": params
        }
        json_string = json.dumps(call_values)
        bytes_to_send = json_string.encode('utf-8')    
        self.client_socket.send(bytes_to_send)
        response = self.client_socket.recv(4096) 
        response_string = response.decode('utf-8')   
        return response_string 

    @staticmethod
    def generate_name() -> str:
        return "ae_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%SZ") + ".csv"
