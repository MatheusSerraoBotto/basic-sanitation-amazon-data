import pandas as pd
import os

# Caminho da pasta com as planilhas
pasta_planilhas = "sheets"
arquivos = [f for f in os.listdir(pasta_planilhas) if f.endswith(".xlsx")]

# Lista para armazenar os dados processados
linhas = []

for arquivo in arquivos:
    caminho = os.path.join(pasta_planilhas, arquivo)
    df = pd.read_excel(caminho, header=2)  # Usa a segunda linha como cabeçalho
    
    # Nome da região está na primeira célula da planilha (linha 0, coluna 0)
    regiao = pd.read_excel(caminho, header=None).iloc[1, 0]

    # Garante que as colunas esperadas existam
    if {"Indicador", "Valor"}.issubset(df.columns):
        # Cria dicionário com região e indicadores
        linha = {"Local": regiao}
        for _, row in df.iterrows():
            indicador = str(row["Indicador"]).strip()
            valor = str(row["Valor"])
            linha[indicador] = valor
        linhas.append(linha)

# Cria o DataFrame final
df_final = pd.DataFrame(linhas)

# Exporta para Excel
df_final.to_excel("brasil.xlsx", index=False)

print("✅ Consolidação concluída! Arquivo salvo como 'consolidado.xlsx'")
