from deta import Deta
import os

deta = Deta('b0zC9ym1tt1d_LBi3rgiGXDyHpGeyX1k1qetPSsSd6Joj')

# This how to connect to or create a drive.
cdn_drive = deta.Drive("nobss_cdn")

def upload_directory(directory_path):
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            file_path = os.path.join(root, file)
            with open(file_path, "rb") as f:
                print(f"Uploading {file}")
                cdn_drive.put(file, f.read())


#upload_directory(r"C:\Users\SeanS\PycharmProjects\NBSRevivedGitHub\static\emulatorjs\data")

#get number of files in deta drive
