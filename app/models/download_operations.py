import os
import gdown


def download_file(url, output_path):
    if os.path.exists(output_path):
        os.remove(output_path)
    gdown.download(url, output_path, quiet=False)
