import os
import gdown
import logging

def download_file(url, output_path):

    try:
        # Verifica se o arquivo já existe e o remove se necessário
        if os.path.exists(output_path):
            os.remove(output_path)
        
        # Baixa o arquivo da URL especificada
        gdown.download(url, output_path, quiet=False)
        logging.info("Download completo: %s", output_path)
    except Exception as e:
        logging.error("Erro durante o download de %s: %s", url, e)
