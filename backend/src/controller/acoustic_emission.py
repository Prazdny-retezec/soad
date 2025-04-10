class AcousticEmissionController:
    def __init__(self, ip_address: str, port: int):
        self.ip_address = ip_address
        self.port = port

    def get_sensors(self) -> list[str]:
        pass

    def is_alive(self) -> bool:
        pass

    def get_time(self) -> int:
        pass

    def configure(self, config: str):
        pass

    def start_recording(self, measurement_name: str, record_history_secs: int):
        pass

    def pause_recording(self):
        pass

    def stop_recording(self):
        pass

    def get_recording_state(self) -> str:
        pass

    def __enter__(self):
        pass

    def __exit__(self):
        pass

    def __call(self):
        pass
