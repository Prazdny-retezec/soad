import win32com.client

# Connect to LabVIEW
labview = win32com.client.Dispatch("LabVIEW.Application")

# Open the specific VI"
vi = labview.GetVIReference("C:\\Users\\david\\Mendelu\\ASS_NSS\\lv_gige\\ConfigAndGrabEdited.vi")

# Set control values - always two parameters ('name of the ui element in LabView', 'value')
# Path to save images from camera
vi.SetControlValue('Path', 'C:\\Users\\david\\Mendelu\\ASS_NSS\\labview-control\\output')
# Interval to save image every x ms
vi.SetControlValue('Interval', 1000)
# Set Camera
#vi.SetControlValue('Camera Name', 'cam0')
# Set Exposure time
vi.SetControlValue('ExposureTime', 850)
# Set width and height
vi.SetControlValue('Width', 800)
vi.SetControlValue('Height', 600)
# Set offset
vi.SetControlValue('OffsetX', 0)
vi.SetControlValue('OffsetY', 0)
# Packet size, DO NOT CHANGE
vi.SetControlValue('Packet size', 8228)

# Run the VI
vi.Run()

error = vi.GetControlValue('error out')
print(f"Output: {error}")

# Close the VI
vi.Close()
