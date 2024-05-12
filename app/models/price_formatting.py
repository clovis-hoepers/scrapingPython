import re

def format_price(price):
    if price is None:
        return None
    if isinstance(price, int):
        return price
    else:
        price = re.sub(r'[^\d.,]', '', price)
    price = price.replace(',', '.')
    if price.count('.') > 1:
        price = price.rsplit('.', 1)[0].replace(
            '.', '') + '.' + price.rsplit('.', 1)[1]
    return '{:.2f}'.format(float(price))
