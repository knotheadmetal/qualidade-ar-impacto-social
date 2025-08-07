import pandas as pd
import os
import json

def load_raw_data(directory):
    """
    Carrega todos os arquivos JSON brutos de um diretório.
    """
    all_data = []
    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            filepath = os.path.join(directory, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
                all_data.append(data)
    return all_data

def transform_air_quality_data(raw_data):
    """
    Realiza a limpeza e transformação dos dados de qualidade do ar.
    """
    processed_records = []
    for record in raw_data:
        if record and record.get("status") == "ok":
            data = record.get("data", {})
            city_info = data.get("city", {})
            iaqi = data.get("iaqi", {})
            time_info = data.get("time", {})

            # Extrair informações básicas
            city_name = city_info.get("name", "N/A")
            aqi = data.get("aqi", None)
            timestamp_iso = time_info.get("iso", None)

            # Extrair poluentes e outras métricas
            pm25 = iaqi.get("pm25", {}).get("v", None)
            pm10 = iaqi.get("pm10", {}).get("v", None)
            no2 = iaqi.get("no2", {}).get("v", None)
            co = iaqi.get("co", {}).get("v", None)
            so2 = iaqi.get("so2", {}).get("v", None)
            o3 = iaqi.get("o3", {}).get("v", None)
            temperature = iaqi.get("t", {}).get("v", None)
            humidity = iaqi.get("h", {}).get("v", None)
            pressure = iaqi.get("p", {}).get("v", None)
            wind = iaqi.get("w", {}).get("v", None)

            processed_records.append({
                "city": city_name,
                "aqi": aqi,
                "timestamp": timestamp_iso,
                "pm25": pm25,
                "pm10": pm10,
                "no2": no2,
                "co": co,
                "so2": so2,
                "o3": o3,
                "temperature": temperature,
                "humidity": humidity,
                "pressure": pressure,
                "wind": wind
            })
    
    df = pd.DataFrame(processed_records)

    # Tratamento de valores ausentes (ex: preencher com 0 ou a média, ou remover)
    # Para este exemplo, vamos preencher valores numéricos ausentes com 0
    numeric_cols = ["aqi", "pm25", "pm10", "no2", "co", "so2", "o3", "temperature", "humidity", "pressure", "wind"]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0) # Converte para numérico e preenche NaN com 0

    # Conversão de tipos
    if "timestamp" in df.columns:
        df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
        df.dropna(subset=["timestamp"], inplace=True) # Remove linhas com timestamp inválido
        if not df.empty and pd.api.types.is_datetime64_any_dtype(df["timestamp"]): # Verifica se o DataFrame não está vazio e se a coluna é datetime
            df["date"] = df["timestamp"].dt.date # Extrai apenas a data
            df["hour"] = df["timestamp"].dt.hour # Extrai a hora

    # Normalização de colunas (ex: garantir que nomes de cidades estejam padronizados)
    if "city" in df.columns:
        df["city"] = df["city"].str.replace(r"\s*\(.*?\)", "", regex=True).str.strip().str.title() # Remove parênteses e capitaliza

    return df

if __name__ == "__main__":
    # Definir os diretórios de forma absoluta para o ambiente do sandbox
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    RAW_DATA_DIR = os.path.join(os.path.dirname(BASE_DIR), "data", "raw")
    PROCESSED_DATA_DIR = os.path.join(os.path.dirname(BASE_DIR), "data", "processed")
    os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)

    print(f"Carregando dados brutos de: {RAW_DATA_DIR}")
    raw_data = load_raw_data(RAW_DATA_DIR)
    print(f"Total de {len(raw_data)} registros brutos carregados.")

    if raw_data:
        print("Iniciando transformação dos dados...")
        transformed_df = transform_air_quality_data(raw_data)
        
        if not transformed_df.empty:
            timestamp_str = pd.Timestamp.now().strftime("%Y%m%d%H%M%S")
            output_filepath = os.path.join(PROCESSED_DATA_DIR, f"air_quality_processed_{timestamp_str}.csv")
            transformed_df.to_csv(output_filepath, index=False)
            print(f"Dados transformados salvos em: {output_filepath}")
        else:
            print("Nenhum dado transformado para salvar.")
    else:
        print("Nenhum dado bruto encontrado para transformar.")


