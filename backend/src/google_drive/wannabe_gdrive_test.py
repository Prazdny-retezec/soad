from google_drive_handler import gdrive_auth, upload_zip_file
from zipper import create_zip_archive, fake_zipper



if __name__ =="__main__":
    measurement_name = "measurement 1"
    zip_file_name = fake_zipper(measurement_name + ".zip")
    gdrive_service = gdrive_auth()
    gdrive_url = upload_zip_file(gdrive_service, path_to_local_zip_file = zip_file_name, gdrive_file_name = measurement_name)