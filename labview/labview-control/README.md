# LabVIEW Controller for PhotonFocus Camera
This script serves to controlling PhotonFocus camera using LabVIEW VI. It allows to pass various parameters for camera setting. Handles **CTRL+C** interuptions to stop and close the VI.

**IMPORTANT** 
Camera has to be connected to machine, then launch the VI file and select it in dropdown. We tried different libraries for python to interact with LabVIEW, but neither of them worked with dropdown camera selection. After selecting the camera the script works.

Also don't forget to change **JUMBO PACKETS** for your Windows PC, therefore change it to the highest in order to receive data from the camera (9014).

## Requirements
- Python 3.x (recommended version: 3.6+)
- win32com.client (requires pywin32 library)
- LabVIEW application installed and accessible via COM automation (enabled ActiveX).

## Installation
1. Create Python Virtual Env
`python -m venv venv`

2. Activate Virtual Env
`. .\venv\Scripts\activate`

3. Install requirements
`pip install -r requirements.txt`

## Args
You can pass the following arguments when running the script:
- `--vi_path`: **Required**. Full path to the LabVIEW VI file (.vi)
- `--image_path`: Path to save the images captured from the camera.
- `--interval`: Interval (in ms) at which the image is saved (default is 100000).
- `--exposure_time`: Exposure time for the camera (default is 850).
- `--width`: Width of the captured image (default is 800).
- `--height`: Height of the captured image (default is 600).
- `--offset_x`: Horizontal offset for image (default is 0).
- `--offset_y`: Vertial offset for image (default is 0).
- `--packet_size`: Packet size for image transmission (default is 8228).

## Usage
`python camera-control.py --vi_path "C:\\path\\to\\your\\VI.vi" --image_path "C:\\path\\to\\save\\image.jpg" --interval 5000 --exposure_time 900 --width 1024 --height 768`

