# Funcionalidade de Extração e Inserção de Dados em MongoDB

## Descrição

Este código realiza a extração de dados de várias URLs, buscando informações como nome e preço de produtos em lojas online, e em seguida insere esses dados em um banco de dados MongoDB. O processo é executado continuamente a cada 30 minutos.

## Estrutura do Projeto

O projeto está estruturado da seguinte maneira:

```
projeto/
│
├── main.py
│
├── utils/
│   ├── web_scraping.py
│   └── mongodb_operations.py
│
└── models/
    ├── data_operations.py
    ├── download_operations.py
    └── price_formatting.py
```

### Arquivos

- `main.py`: O arquivo principal que inicia o processo de extração e inserção de dados.
- `utils/web_scraping.py`: Contém funções para extrair dados de URLs usando web scraping.
- `utils/mongodb_operations.py`: Contém funções para inserir dados em um banco de dados MongoDB.
- `models/data_operations.py`: Contém funções para carregar URLs de um arquivo.
- `models/download_operations.py`: Contém funções para baixar um arquivo de uma URL.
- `models/price_formatting.py`: Contém uma função para formatar o preço extraído.

## Funcionalidades

1. **Extração de Dados (web_scraping.py)**:
   - Utiliza a biblioteca `requests` para realizar solicitações HTTP às URLs.
   - Utiliza a biblioteca `BeautifulSoup` para analisar o HTML das páginas.
   - Extrai o nome e o preço dos produtos das páginas HTML.
   - Formata o preço extraído.

2. **Operações de Banco de Dados (mongodb_operations.py)**:
   - Utiliza a biblioteca `pymongo` para se conectar e interagir com um banco de dados MongoDB.
   - Insere os dados extraídos (nome, preço e URL) no banco de dados MongoDB.
   - Adiciona a data e hora de inserção dos dados.

3. **Operações de Arquivos (data_operations.py, download_operations.py)**:
   - `data_operations.py`:
     - Carrega URLs de um arquivo de texto.
   - `download_operations.py`:
     - Baixa um arquivo de uma URL, substituindo o arquivo existente, se houver.

4. **Execução Contínua (main.py)**:
   - Inicia o processo de extração e inserção de dados em um loop contínuo.
   - Baixa o arquivo de URLs de uma fonte externa.
   - Carrega as URLs do arquivo.
   - Para cada URL, extrai os dados, formata-os e insere-os no banco de dados MongoDB.
   - Aguarda 30 minutos antes de começar o próximo ciclo.

## Execução

Para executar o código, basta rodar o arquivo `main.py`. Certifique-se de ter todas as dependências instaladas, como `requests`, `beautifulsoup4`, `pymongo` e `gdown`.

```bash
python main.py
```

O código irá executar continuamente, atualizando o banco de dados MongoDB com os dados extraídos de todas as URLs listadas no arquivo `urls.txt`.
