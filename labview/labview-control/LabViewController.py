import win32com.client
import sys

class LabVIEWController:
    def __init__(self, vi_path):
        """
        Initialize the LabVIEWController and connect to the LabVIEW application.
        """
        self.vi_path = vi_path
        self.labview = win32com.client.Dispatch("LabVIEW.Application")
        self.vi = None

    def open_vi(self):
        """
        Open the specific VI.
        """
        self.vi = self.labview.GetVIReference(self.vi_path)

    def set_controls(self, path, interval, exposure_time, width, height, offset_x, offset_y, packet_size):
        """
        Set control values for the VI.
        """
        self.vi.SetControlValue('Path', path)
        self.vi.SetControlValue('Interval', interval)
        self.vi.SetControlValue('ExposureTime', exposure_time)
        self.vi.SetControlValue('Width', width)
        self.vi.SetControlValue('Height', height)
        self.vi.SetControlValue('OffsetX', offset_x)
        self.vi.SetControlValue('OffsetY', offset_y)
        self.vi.SetControlValue('Packet size', packet_size)

    def run(self):
        """
        Run the VI.
        """
        self.vi.Run()

    def get_error(self):
        """
        Get the error status from the VI.
        """
        return self.vi.GetControlValue('error out')

    def stop(self):
        """
        Stop the VI by simulating pressing the stop button.
        """
        self.vi.SetControlValue('STOP', True)

    def close(self):
        """
        Close the VI.
        """
        self.vi.Close()

    def handle_interrupt(self):
        """
        Handle KeyboardInterrupt (Ctrl+C) to stop and close the VI.
        """
        print("\nInterrupted by user. Stopping and closing VI...")
        self.stop()
        self.close()
        sys.exit(0)