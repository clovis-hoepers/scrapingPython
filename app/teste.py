import requests
url = "https://www.terabyteshop.com.br/produto/28528/placa-de-video-msi-nvidia-geforce-rtx-4070-super-ventus-3x-oc-12gb-gddr6x-dlss-ray-tracing-912-v513-643?gad_source=4&gclid=CjwKCAjw3NyxBhBmEiwAyofDYf1kCZjGKQJLMY-GqGKs-3CACOQDLG4ALzmWPbcpNSDskdxJff8I4xoCFVAQAvD_BwE"
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
result = requests.get(url, headers=headers)
print(result.content.decode())