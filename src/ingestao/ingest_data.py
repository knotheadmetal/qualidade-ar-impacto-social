import requests
import pandas as pd
import os
import json

API_TOKEN = '59a68fee67369cb1c521c1147d5916696078d394'
BASE_URL = 'http://api.waqi.info/feed/'

# Diretório para armazenar os dados brutos
RAW_DATA_DIR = '/home/ubuntu/projeto_qualidade_ar/data/raw'
os.makedirs(RAW_DATA_DIR, exist_ok=True)

def get_air_quality_data(city, token):
    """
    Coleta dados de qualidade do ar para uma cidade específica da API WAQI.
    """
    url = f'{BASE_URL}{city}/?token={token}'
    try:
        response = requests.get(url)
        response.raise_for_status()  # Levanta um erro para códigos de status HTTP ruins (4xx ou 5xx)
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f'Erro ao buscar dados para {city}: {e}')
        return None

def save_data_to_json(data, city_name, directory):
    """
    Salva os dados coletados em um arquivo JSON.
    """
    if data:
        filepath = os.path.join(directory, f'{city_name}_air_quality_{pd.Timestamp.now().strftime("%Y%m%d%H%M%S")}.json')
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f'Dados de {city_name} salvos em {filepath}')

if __name__ == '__main__':
    cities = ['shanghai', 'london', 'new-york'] # Exemplo de lista de cidades

    for city in cities:
        print(f'Coletando dados para {city}...')
        air_quality_data = get_air_quality_data(city, API_TOKEN)
        if air_quality_data:
            save_data_to_json(air_quality_data, city, RAW_DATA_DIR)
        print('-' * 30)


