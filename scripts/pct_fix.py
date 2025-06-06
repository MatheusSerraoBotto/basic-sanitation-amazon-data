import pandas as pd

# Configurações
arquivo_csv = 'brasil5.csv'  # Nome do arquivo CSV
coluna_alvo = 'Parcela da população sem coleta de esgoto'  # Coluna com os valores a serem corrigidos
saida_csv = 'brasil6tes.csv'  # Nome do arquivo de saída

# Função de correção
def corrigir_porcentagem(valor):
    try:
        # Manter valores nulos representados por '-'
        if valor == '-':
            return valor
        
        # Converter para float se possível
        num = float(valor)
        
        # Manter valores entre 0 e 1
        if 0 <= num <= 1:
            return num
        
        # Corrigir valores acima de 1
        if num > 1:
            return num / 1000
        
        # Tratar valores negativos (opcional)
        if num < 0:
            return 0.0  # Ou outra ação desejada
            
    except (ValueError, TypeError):
        # Caso não seja conversível para número
        return valor  # Mantém o valor original

# Ler o arquivo CSV
try:
    df = pd.read_csv(arquivo_csv, dtype={coluna_alvo: str})
    
    # Aplicar correções na coluna especificada
    df[coluna_alvo] = df[coluna_alvo].apply(corrigir_porcentagem)

    print(df[coluna_alvo].head(20))  # Exibir as primeiras linhas para verificação
    
    # Salvar arquivo corrigido
    df.to_csv(saida_csv, index=False)
    print(f"✅ Correções aplicadas com sucesso! Arquivo salvo como: {saida_csv}")

except Exception as e:
    print(f"⚠️ Erro durante o processamento: {str(e)}")