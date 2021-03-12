"""
Common Utilities used in Day to Day Programming.
A Python Programmers Bread and Butter.
Author : Farhan Hai Khan
Github : @khanfarhan10
Original File at : https://github.com/khanfarhan10/custom_utils/
"""
import os
import zipfile
import os
import shutil


def create_dir(dir, v=1):
    """
    Creates a directory without throwing an error if directory already exists.
    dir : The directory to be created.
    v : Verbosity
    """
    if not os.path.exists(dir):
        os.makedirs(dir)
        if v:
            print("Created Directory : ", dir)
        return 1
    else:
        if v:
            print("Directory already existed : ", dir)
        return 0


def DeleteFolderContents(dir):
    """
    Cleans the Directory by removing all Folder Contennts
    """
    create_dir(dir)
    shutil.rmtree(dir)
    create_dir(dir)


"""
Utility for Compressing Directories to .zip file
zipper('/content/MAIN/Train', "Zipped_Data.zip")
"""


def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file))


def zipper(dir_path, zip_path):
    zipf = zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED)
    zipdir(dir_path, zipf)
    zipf.close()
