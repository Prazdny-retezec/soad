import zipfile
import glob

# TODO add error handling 
def create_zip_archive(list_of_files, zip_destination_name_path):
    with zipfile.ZipFile(zip_destination_name_path, 'w') as new_zip:
        for file in list_of_files:
            print(file)
            new_zip.write(file)


def fake_zipper(zip_file_name="sample.zip"):
    list_of_files = glob.glob("../../mock_data/*/*")
    create_zip_archive(list_of_files, zip_file_name)
    return zip_file_name

