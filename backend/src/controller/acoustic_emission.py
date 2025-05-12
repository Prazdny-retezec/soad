from datetime import datetime

import socket
import json

#TODO error validation either via response operation status parameter or something else

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
    #https://bitbucket.org/dakel/node-zedo-rpc/src/master/API.md#configure
    def configure(self, config: str): #config by mal byt imo objekt, TODO prerobit
        params = {
            "config": config,
            "verbosity": "all",
        }
        return self.__call("Configure", params=params)

    def start_recording(self, measurement_name: str, record_history_secs: int):
        params = {
            "measurement_name": measurement_name,
            "record_history_secs": record_history_secs,
        }
        self.__call("StartRecording", params=params)

    def pause_recording(self):
        self.__call("PauseRecording")

    def stop_recording(self):
        self.__call("StopRecording")
    
    def export_ae_data(self):
        #TODO imo treba file reader setup, z GetFileReaderData sa pravdepodobne ziska ten name
        '''
        params = {
            "reader_id": reader_id,
            "outdir": self.output_dir,
            "subdir": subdir,
            "export_cfg": export_cfg,
            "make_unique_dir": make_unique_dir,
        }
        self.__call("ExportFileReaderData", params=params)
        '''
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
        #yoink 
        # Vytvoření slovníku s hodnotami pro volání
        call_values = {
            'jsonrpc': '2.0', 
            'method': method, 
            'id': id,
            "params": params
        }

        # Převod slovníku na řetězec JSON
        json_string = json.dumps(call_values)

        # Převod řetězce JSON na bajty
        bytes_to_send = json_string.encode('utf-8')    

        # Odeslání bajtů přes socket
        self.client_socket.send(bytes_to_send)
        response = self.client_socket.recv(4096)  # Přečte až 4096 bajtů (můžete upravit podle potřeby)

        # Převod bajtů na řetězec
        response_string = response.decode('utf-8')   
        return response_string 

    @staticmethod
    def generate_name() -> str:
        return "ae_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%SZ") + ".csv"
