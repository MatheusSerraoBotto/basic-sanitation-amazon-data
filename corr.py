import pandas as pd
from ydata_profiling import ProfileReport

import seaborn as sns
import matplotlib.pyplot as plt


df = pd.read_csv('cities8.csv')

df = df[df['Amazonia'] == 'Sim']
print(df.columns)
# drop colums Cidade,Estado,ID,Latitude,Longitude,Amazonia
df = df.drop(columns=['Cidade', 'Estado', 'ID', 'Latitude', 'Longitude', 'Amazonia'])
# # Calcular matriz de correlação
corr_matrix = df.corr(numeric_only=True)

# Visualizar como heatmap
plt.figure(figsize=(12, 8))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5)
plt.title("Matriz de Correlação")
plt.show()

# convertendo a matriz de correlação em um DataFrame
corr_df = pd.DataFrame(corr_matrix)
# salvar a matriz de correlação em um arquivo CSV
corr_df.to_csv('correlacao.csv', index=True)

# profile = ProfileReport(df, title="Análise de Correlação")
# profile.to_file("correlacao.html")  # Relatório interativo