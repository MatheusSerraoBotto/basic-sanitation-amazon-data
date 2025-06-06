import pandas as pd
import os
import re

# Configurações
pasta_planilhas = './sheets/sheets_cities'  # Pasta onde estão as planilhas auxiliares
arquivo_principal = 'cities3.csv'  # Arquivo principal com dados dos municípios
arquivo_saida = 'cities8.csv'      # Arquivo de saída

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
    # Saneamento básico - acesso e infraestrutura
    'Parcela da população sem acesso à água': ('Parcela da população sem acesso à água', 'SNIS'),
    'Parcela da população com acesso à água': ('Parcela da população com acesso à água', 'SNIS'),
    'População com acesso à água': ('População com acesso à água', 'SNIS'),
    'População sem acesso à água': ('População sem acesso à água', 'SNIS'),
    'Parcela da população sem coleta de esgoto': ('Parcela da população sem coleta de esgoto', 'SNIS'),
    'Parcela da população com coleta de esgoto': ('Parcela da população com coleta de esgoto', 'SNIS'),
    'População com coleta de esgoto': ('População com coleta de esgoto', 'SNIS'),
    'População sem coleta de esgoto': ('População sem coleta de esgoto', 'SNIS'),
    'Parcela das moradias sem banheiro': ('Parcela das moradias sem banheiro', 'IBGE'),
    'Parcela das moradias com banheiro': ('Parcela das moradias com banheiro', 'IBGE'),
    'Moradias com banheiro': ('Moradias com banheiro', 'IBGE'),
    'Moradias sem banheiro': ('Moradias sem banheiro', 'IBGE'),

    # Saneamento e desigualdade racial
    'Percentagem da população branca sem acesso à água': ('Percentagem da população branca sem acesso à água', 'IBGE'),
    'Percentagem da população preta sem acesso à água': ('Percentagem da população preta sem acesso à água', 'IBGE'),
    'Percentagem da população amarela sem acesso à água': ('Percentagem da população amarela sem acesso à água', 'IBGE'),
    'Percentagem da população parda sem acesso à água': ('Percentagem da população parda sem acesso à água', 'IBGE'),
    'Percentagem da população indígena sem acesso à água': ('Percentagem da população indígena sem acesso à água', 'IBGE'),
    'Percentagem da população branca sem acesso à coleta de esgoto': ('Percentagem da população branca sem acesso à coleta de esgoto', 'IBGE'),
    'Percentagem da população preta sem acesso à coleta de esgoto': ('Percentagem da população preta sem acesso à coleta de esgoto', 'IBGE'),
    'Percentagem da população amarela sem acesso à coleta de esgoto': ('Percentagem da população amarela sem acesso à coleta de esgoto', 'IBGE'),
    'Percentagem da população parda sem acesso à coleta de esgoto': ('Percentagem da população parda sem acesso à coleta de esgoto', 'IBGE'),
    'Percentagem da população indígena sem acesso à coleta de esgoto': ('Percentagem da população indígena sem acesso à coleta de esgoto', 'IBGE'),

    # Saúde pública (diretamente ligadas ao saneamento)
    'Incidência de internações por diarreia': ('Incidência de internações por diarreia', 'DATASUS'),
    'Internações por diarreia': ('Internações por diarreia', 'DATASUS'),
    'Internações por doenças de veiculação hídrica': ('Internações por doenças de veiculação hídrica', 'DATASUS'),
    'Incidência de internações totais por doenças de veiculação hídrica': ('Incidência de internações totais por doenças de veiculação hídrica', 'DATASUS'),
    'Óbitos por doenças de veiculação hídrica': ('Óbitos por doenças de veiculação hídrica', 'DATASUS'),
    'Taxa de óbitos por doenças de veiculação hídrica': ('Taxa de óbitos por doenças de veiculação hídrica', 'DATASUS'),
    'Despesas com internações por doenças de veiculação hídrica': ('Despesas com internações por doenças de veiculação hídrica', 'DATASUS'),

    # Saúde pública (respiratórias – podem indicar impacto indireto)
    'Internações por doenças respiratórias': ('Internações por doenças respiratórias', 'DATASUS'),
    'Incidência de internações por doenças respiratórias': ('Incidência de internações por doenças respiratórias', 'DATASUS'),
    'Óbitos por doenças respiratórias': ('Óbitos por doenças respiratórias', 'DATASUS'),
    'Incidência de óbitos por doenças respiratórias': ('Incidência de óbitos por doenças respiratórias', 'DATASUS'),

    # Eficiência e qualidade dos serviços
    'Consumo per capita de água': ('Consumo per capita de água', 'SNIS'),
    'Índice de esgoto tratado referido à água consumida': ('Índice de esgoto tratado referido à água consumida', 'SNIS'),
    'Perdas na distribuição': ('Perdas na distribuição', 'SNIS'),
    'Perdas no faturamento': ('Perdas no faturamento', 'SNIS'),
    
    # Capacidade e cobertura
    'Extensão da rede de água': ('Extensão da rede de água', 'SNIS'),
    'Extensão da rede de esgoto': ('Extensão da rede de esgoto', 'SNIS'),

    # Investimentos e recursos
    'Investimentos totais, em R$ de 2022': ('Investimentos totais, em R$ de 2022', 'ITB'),
    'Investimentos per capita, em R$ de 2022': ('Investimentos per capita, em R$ de 2022', 'ITB'),
    'Despesas per capita com saneamento': ('Despesas per capita com saneamento', 'SNIS'),
    'Tarifa de água': ('Tarifa de água', 'SNIS'),
    'Tarifa de coleta de esgoto': ('Tarifa de coleta de esgoto', 'SNIS'),

    # Urbanismo e estrutura populacional
    'Densidade demográfica': ('Densidade demográfica', 'IBGE'),
    'Densidade domiciliar': ('Densidade domiciliar', 'IBGE'),
    'População': ('População', 'IBGE'),
    'Área do município': ('Área do município', 'IBGE'),
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