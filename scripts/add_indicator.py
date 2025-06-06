import pandas as pd
import os
import re

# Configurações
pasta_planilhas = './sheets/sheets_cities'  # Pasta onde estão as planilhas auxiliares
arquivo_principal = 'cities6.csv'  # Arquivo principal com dados dos municípios
arquivo_saida = 'cities7.csv'      # Arquivo de saída

# Função para sanitizar nomes de arquivo
def sanitizar_nome(nome):
    return re.sub(r'[\\/*?:"<>|]', '_', nome)

# Função para extrair valor de indicador
def extrair_indicador(df_aux, indicador, fonte=None):
    try:
        # Filtrar por indicador e fonte
        filtro = (df_aux['Indicador'].str.strip().str.lower() == indicador.lower())
        if fonte:
            filtro = filtro & (df_aux['Fonte'].str.strip().str.lower() == fonte.lower())
        
        # Obter o valor
        resultado = df_aux.loc[filtro, 'Valor'].iloc[0]

        if resultado == '-':
            return None

        return resultado
    
    except (IndexError, KeyError):
        return None
    except Exception:
        return None

# Carregar DataFrame principal
df_principal = pd.read_csv(arquivo_principal)

# Dicionário de indicadores para adicionar
indicadores = {
    'Densidade demográfica': ('Densidade demográfica', 'IBGE'),
    'Área do município': ('Área do município', 'IBGE'),
    'Receita direta e indireta total': ('Receita direta e indireta total', 'SNIS'),
    'Parcela das moradias sem banheiro': ('Parcela das moradias sem banheiro', 'IBGE'),
    'Incidência de internações por diarreia': ('Incidência de internações por diarreia', 'DATASUS'),
    'Taxa de óbitos por doenças de veiculação hídrica': ('Taxa de óbitos por doenças de veiculação hídrica', 'DATASUS'),
    'Consumo per capita de água': ('Consumo per capita de água', 'SNIS'),
    'Perdas na distribuição': ('Perdas na distribuição', 'SNIS'),
    'Índice de esgoto tratado referido à água consumida': ('Índice de esgoto tratado referido à água consumida', 'SNIS'),
    'Tarifa de água': ('Tarifa de água', 'SNIS'),
    'Custo com energia elétrica': ('Custo com energia elétrica', 'SNIS'),
    'Incidência de internações totais por doenças de veiculação hídrica' : ('Incidência de internações totais por doenças de veiculação hídrica', 'DATASUS'),
    'Moradias sem banheiro': ('Moradias sem banheiro', 'IBGE'),
}

# Processar cada linha do DataFrame principal
for idx, linha in df_principal.iterrows():
    if linha['Amazonia'] == 'Não':
        continue  

    # Construir nome do arquivo auxiliar (exemplo: "Ariquemes_2022.csv")
    city = linha['Cidade']
    state = linha['Estado']
    id = linha['ID']
    
    nome_arquivo = f"{id}_{city}_{state}.xlsx"
    caminho_arquivo = os.path.join(pasta_planilhas, nome_arquivo)
    
    # Verificar se arquivo existe
    if not os.path.exists(caminho_arquivo):
        continue
    
    try:
        # Carregar planilha auxiliar
        df_aux = pd.read_excel(
            caminho_arquivo,
            skiprows=2
        )
        
        # Renomear colunas para padronização
        df_aux.columns = [col.strip() for col in df_aux.columns]
        
        # Adicionar cada indicador ao DataFrame principal
        for coluna, (indicador, fonte) in indicadores.items():
            valor = extrair_indicador(df_aux, indicador, fonte)
            
            # Criar coluna se não existir
            if coluna not in df_principal.columns:
                df_principal[coluna] = ''
                
            # Atualizar valor
            df_principal.at[idx, coluna] = valor
    
    except Exception as e:
        print(f"⚠️ Erro no arquivo {nome_arquivo}: {str(e)}")

# Salvar resultado
df_principal.to_csv(arquivo_saida, index=False)
print(f"✅ Dados enriquecidos salvos em: {arquivo_saida}")

print(df_principal.head())  # Exibir as primeiras linhas do DataFrame resultante