import os
import tempfile
import subprocess
from google.cloud import storage


def is_file_valid(file_path):
    if not os.path.isfile(file_path):
        return False

    try:
        with open(file_path, 'rb') as f:
            # Try to read some data from the file
            f.read(1)
            return True
    except Exception as e:
        print(f"Invalid file: {e}")
        return False

def copy_file(data, context):
    file_name = data["name"]
    print(f"Processing file: {file_name}")

    client = storage.Client()
    bucket = client.bucket(data["bucket"])
    blob = bucket.blob(file_name)

    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        blob.download_to_file(temp_file)
        temp_file_path = temp_file.name
        destination_path = f"/tmp/{file_name}"

        if not is_file_valid(temp_file_path):
            print(f"File {file_name} is not valid, skipping processing")
            return

        os.environ['FILEENV'] = f"{file_name}"
        os.rename(temp_file_path, destination_path)

    print(f"File {file_name} copied to {destination_path}")
    subprocess.call(["python", "process.py"])


