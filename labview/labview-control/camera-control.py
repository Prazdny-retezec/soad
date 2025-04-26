import argparse
import signal
from LabViewController import LabVIEWController

def validate_vi_path(vi_path):
    """
    Validate the VI path to ensure it ends with '.vi'.
    """
    if not vi_path.endswith('.vi'):
        raise Exception(f"Error: The VI path must end with '.vi'. Provided path: {vi_path}")

def main():
    """
    Main function to parse arguments, run the LabVIEW VI, and handle user interruption.
    """
    parser = argparse.ArgumentParser(description="Control LabVIEW VI from Python.")
    parser.add_argument('--vi_path', type=str, default='', help="Path where VI is located.")
    parser.add_argument('--image_path', type=str, default='', help="Path to save images from the camera.")
    parser.add_argument('--interval', type=int, default=100000, help="Interval (in ms) to save image.")
    parser.add_argument('--exposure_time', type=int, default=850, help="Exposure time for the camera.")
    parser.add_argument('--width', type=int, default=800, help="Width of the image.")
    parser.add_argument('--height', type=int, default=600, help="Height of the image.")
    parser.add_argument('--offset_x', type=int, default=0, help="Offset X for the image.")
    parser.add_argument('--offset_y', type=int, default=0, help="Offset Y for the image.")
    parser.add_argument('--packet_size', type=int, default=8228, help="Packet size (should not be changed).")

    args = parser.parse_args()

    signal.signal(signal.SIGINT, lambda signal, frame: controller.handle_interrupt())

    try:

        validate_vi_path(args.vi_path)
        controller = LabVIEWController(args.vi_path)
        controller.open_vi()

        controller.set_controls(args.image_path, args.interval, args.exposure_time, args.width, args.height, args.offset_x, args.offset_y, args.packet_size)

        controller.run()

        error = controller.get_error()
        print(f"Output: {error}")

        controller.close()

    except KeyboardInterrupt:
        controller.handle_interrupt()

if __name__ == "__main__":
    main()