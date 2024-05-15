import os
import pandas as pd

def load_urls_from_file(file_path):

    try:
        # Verifica se o caminho do arquivo é válido
        if not os.path.exists(file_path):
            raise FileNotFoundError(f'O arquivo {file_path} não foi encontrado.')
        
        # Carrega o arquivo CSV em um DataFrame
        with open(file_path, 'r') as file:
            df = pd.read_csv(file, header=None, names=['URL'])
        
        # Retorna a lista de URLs
        return df['URL'].tolist()
    
    except Exception as e:
        # Captura exceções e registra em log
        print(f"Erro ao carregar URLs do arquivo: {e}")
        return []
