import pandas as pd
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable
import time # Para adicionar pausas entre as requisições
import re # Para limpar os nomes das cidades

# --- Configurações ---
# Nome do arquivo de entrada (altere se necessário)
# Vou assumir que você quer usar o 'download (1).csv' que foi mencionado anteriormente.
INPUT_CSV_FILE = 'cities.xlsx' # Altere para o nome correto do arquivo de entrada
OUTPUT_CSV_FILE = 'cities2.csv' # Nome do arquivo de saída

# Nomes das colunas conforme sua solicitação
CITY_COLUMN = 'Cidade'
STATE_COLUMN = 'Estado'
NEW_LAT_COLUMN = 'Latitude' # Novo nome para evitar conflito se já existirem
NEW_LON_COLUMN = 'Longitude'# Novo nome para evitar conflito se já existirem

# --- Script Principal ---
try:
    df = pd.read_excel(INPUT_CSV_FILE)
except FileNotFoundError:
    print(f"Erro: O arquivo '{INPUT_CSV_FILE}' não foi encontrado. Verifique o nome e o caminho do arquivo.")
    exit()
except Exception as e:
    print(f"Erro ao carregar o arquivo CSV: {e}")
    exit()

print(f"Usando as colunas: Cidade='{CITY_COLUMN}', Estado='{STATE_COLUMN}'")

# Criar as novas colunas de latitude e longitude, inicializadas com None
df[NEW_LAT_COLUMN] = None
df[NEW_LON_COLUMN] = None

# Inicializar o geolocalizador Nominatim
# É importante definir um user_agent único para sua aplicação
geolocator = Nominatim(user_agent="my_geocoding_app_v1") # Mude "my_geocoding_app_v1" para algo único

print(f"Iniciando geocodificação. Total de linhas a processar: {len(df)}")
successful_geocodes = 0
failed_geocodes = 0

# Iterar sobre as linhas do DataFrame
for index, row in df.iterrows():

    cleaned_city = row[CITY_COLUMN]
    state = row[STATE_COLUMN]

    # Só processar se o estado estiver preenchido
    if pd.notna(state) and str(state).strip():
        if pd.notna(cleaned_city) and str(cleaned_city).strip():
            query = f"{cleaned_city}, {state}, Brasil"
            print(f"Processando ({index + 1}/{len(df)}): {query} ... ", end="")
            
            try:
                # Fazer a requisição de geocodificação
                location = geolocator.geocode(query, timeout=10) # timeout de 10 segundos

                if location:
                    df.loc[index, NEW_LAT_COLUMN] = location.latitude
                    df.loc[index, NEW_LON_COLUMN] = location.longitude
                    print(f"Encontrado: Lat={location.latitude:.4f}, Lon={location.longitude:.4f}")
                    successful_geocodes += 1
                else:
                    print("Não encontrado.")
                    failed_geocodes += 1
            
            except GeocoderTimedOut:
                print("Tempo esgotado na requisição (Timed out).")
                failed_geocodes += 1
            except GeocoderUnavailable:
                print("Serviço indisponível no momento.")
                failed_geocodes += 1
            except Exception as e:
                print(f"Erro inesperado: {e}")
                failed_geocodes += 1
            
            # IMPORTANTE: Pausa para respeitar a política de uso do Nominatim (1 req/seg)
            time.sleep(1.1) # Um pouco mais de 1 segundo para segurança
            
        else:
            # print(f"Linha {index + 1}: Nome da cidade ('{CITY_COLUMN}') ausente, pulando.")
            pass # Cidade ausente, mas estado preenchido, não faz nada
    else:
        # print(f"Linha {index + 1}: Nome do estado ('{STATE_COLUMN}') ausente, pulando geocodificação.")
        pass # Estado ausente, não faz nada

print("\n--- Resumo da Geocodificação ---")
print(f"Coordenadas encontradas com sucesso: {successful_geocodes}")
print(f"Falhas ou não encontradas: {failed_geocodes}")
print(f"Linhas não processadas (sem estado): {len(df) - (successful_geocodes + failed_geocodes)}")

# Salvar o DataFrame modificado
try:
    df.to_csv(OUTPUT_CSV_FILE, index=False, encoding='utf-8')
    print(f"\nPlanilha processada e salva como '{OUTPUT_CSV_FILE}'.")
except Exception as e:
    print(f"Erro ao salvar o arquivo CSV: {e}")