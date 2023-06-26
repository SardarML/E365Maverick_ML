import py7zr
import os

def zip_folder(folder_path, zip_path):
    with py7zr.SevenZipFile(zip_path, 'w') as zipf:
        zipf.writeall(folder_path, arcname=os.path.basename(folder_path))

# path to the folder you want to zip
folder_path = 'folder_path'

# path to the 7z file to be created
zip_path = 'folder_path.7z'

# convert folder to 7z
zip_folder(folder_path, zip_path)