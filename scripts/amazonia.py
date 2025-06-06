import pandas as pd

# Defina aqui as coordenadas aproximadas da "caixa" que representa a Amazônia Legal.
# Estes valores são EXEMPLOS e precisam ser ajustados para maior precisão ou
# substituídos por uma verificação de polígono mais exata.
# Formato: [longitude_minima, latitude_minima, longitude_maxima, latitude_maxima]
# Essas coordenadas são uma aproximação muito grosseira da bacia amazônica no Brasil.
# Longitude Oeste é negativa, Latitude Sul é negativa.

df_amazonia_legal = pd.read_excel('Municipios_da_Amazonia_Legal_2022.xlsx')
# create tuple NM_UF e NM_MUN
cities = set(zip(df_amazonia_legal["NM_MUN"], df_amazonia_legal["NM_UF"]))

def verificar_se_na_amazonia_aproximado(name, state):
    val = (name, state)
    if val in cities:
        return "Sim"
    else:
        return "Não"
    
def processar_csv_cidades(caminho_do_arquivo_csv):
    """
    Lê um arquivo CSV, verifica se cada cidade está na Amazônia Legal (aproximado)
    e adiciona uma nova coluna com essa informação.

    Args:
        caminho_do_arquivo_csv (str): O caminho para o arquivo CSV.

    Returns:
        pandas.DataFrame: O DataFrame original com uma nova coluna 'na_amazonia_legal_aprox'.
                          Retorna None se o arquivo não for encontrado ou as colunas não existirem.
    """
    try:
        df = pd.read_csv(caminho_do_arquivo_csv)
    except FileNotFoundError:
        print(f"Erro: Arquivo '{caminho_do_arquivo_csv}' não encontrado.")
        return None
    except Exception as e:
        print(f"Erro ao ler o CSV: {e}")
        return None
    
    import re
    def clean_name(name):
        return re.sub(r'\s*\((Município|Distrito|Vila)\)$', '', name, flags=re.IGNORECASE).strip()

    # Aplica a função para cada linha do DataFrame
    df['Amazonia'] = df.apply(
        lambda row: verificar_se_na_amazonia_aproximado(row["Cidade"], row["Estado"]),
        axis=1
    )

    return df

# --- Exemplo de Uso ---
if __name__ == "__main__":
    # Crie um arquivo CSV de exemplo chamado 'cidades.csv' com o seguinte conteúdo:
    #
    # nome_cidade,latitude,longitude
    # Manaus,-3.1190278,-60.0217278
    # São Paulo,-23.55052,-46.633308
    # Belém,-1.45502,-48.50237
    # Rio de Janeiro,-22.906847,-43.172896
    # Cuiabá,-15.6014,-56.0979
    # Porto Velho,-8.76194,-63.9039
    # Boa Vista,2.82352,-60.67583
    # Macapá,0.0349,-51.0694
    # Palmas,-10.2492,-48.3244
    # São Luís,-2.53874,-44.2825
    # Miami,25.761681,-80.191788
    # Cidade Nula,,
    #
    # Salve este conteúdo em um arquivo chamado 'cidades.csv' no mesmo diretório do script.

    caminho_csv = 'cities2.csv'  # Nome do seu arquivo CSV

    df_resultado = processar_csv_cidades(caminho_csv)

    if df_resultado is not None:
        print("\nResultado do processamento:")
        print(df_resultado)

        # Para salvar o resultado em um novo CSV:
        df_resultado.to_csv('cities3.csv', index=False)
        # print("\nDataFrame resultante salvo em 'cidades_com_info_amazonia.csv'")