import re

def format_price(price):

    try:
        if price is None:
            return None
        
        # Verifica se a entrada é uma string válida
        if not isinstance(price, str):
            raise ValueError("O preço deve ser uma string.")
        
        # Remove todos os caracteres não numéricos, exceto ponto e vírgula
        price = re.sub(r'[^\d.,]', '', price)
        
        # Substitui vírgulas por pontos para garantir o formato float
        price = price.replace(',', '.')
        
        # Se houver mais de um ponto decimal, remove todos exceto o último
        if price.count('.') > 1:
            price = price.rsplit('.', 1)[0].replace('.', '') + '.' + price.rsplit('.', 1)[1]
        
        # Formata o preço para duas casas decimais
        return '{:.2f}'.format(float(price))
    except Exception as e:
        # Captura exceções e registra em log
        print(f"Erro ao formatar o preço: {e}")
        return None
