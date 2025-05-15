import csv
import os
import threading
import random
import time
from datetime import datetime, timedelta

from controller.acoustic_emission import AcousticEmissionController


class AcousticEmissionMockController(AcousticEmissionController):

    def __init__(self, ip_address: str, port: int, output_dir: str):
        super().__init__(ip_address, port, output_dir)

        self._data = []
        self._is_running = False
        self._thread = None

    def start_recording(self, measurement_name: str, record_history_secs: int):
        if self._is_running:
            return

        self._is_running = True
        self._data = []
        self._thread = threading.Thread(target=self._generate_data)
        self._thread.start()

    def stop_recording(self):
        self._is_running = False
        if self._thread:
            self._thread.join()

        filename = AcousticEmissionController.generate_name()
        with open(os.path.join(self.output_dir, filename), mode="w", newline="\n") as file:
            writer = csv.writer(file, delimiter='\t')
            for row in self._data:
                writer.writerow(row)

    def _generate_data(self):
        current_time = datetime.now()
        while self._is_running:
            value1 = random.choices([0, 1, 2, 3, 4, 5, 11, 522], weights=[40, 10, 10, 5, 5, 3, 2, 1])[0]
            value2 = 0
            value3 = round(random.uniform(72.242, 162.515), 3)

            timestamp_str = current_time.strftime("%Y/%m/%d %H:%M:%S.%f")[:-3]
            self._data.append([timestamp_str, value1, value2, value3])

            time.sleep(1)
            current_time += timedelta(seconds=1)

    def configure(self, config: str):
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass