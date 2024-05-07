import pandas as pd


def load_urls_from_file(file_path):
    df = pd.read_csv(file_path, header=None, names=['URL'])
    return df['URL'].tolist()
