from bs4 import BeautifulSoup
import pandas as pd

# O HTML fornecido como uma string multilinha
# (Em um caso real, você poderia carregar isso de um arquivo ou de uma resposta de requisição web)
html_content2 = """
<ul> # Adicionei um UL pai para simular uma lista completa de estados
    <li class="sublist--item">
        <a class="link" data-level="2" role="button">
            <span>Acre</span>
            <span class="icon icon-arrow-right"></span>
        </a>
        <div class="sublist--list">
            <h1 class="title">Acre</h1>
            <ul class="sublist--list" data-last="">
                <li class="sublist--item">
                    <a class="link" href="/localidade?id=120020">
                        <span>Cruzeiro do Sul</span>
                    </a>
                </li>
                <li class="sublist--item">
                    <a class="link" href="/localidade?id=120040">
                        <span>Rio Branco</span>
                    </a>
                </li>
            </ul>
        </div>
    </li>
    <li class="sublist--item">
        <a class="link" data-level="2" role="button">
            <span>Alagoas</span>
            <span class="icon icon-arrow-right"></span>
        </a>
        <div class="sublist--list">
            <h1 class="title">Alagoas</h1>
            <ul class="sublist--list" data-last="">
                <li class="sublist--item">
                    <a class="link" href="/localidade?id=270030">
                        <span>Arapiraca</span>
                    </a>
                </li>
                <li class="sublist--item">
                    <a class="link" href="/localidade?id=270430">
                        <span>Maceió</span>
                    </a>
                </li>
            </ul>
        </div>
    </li>
    {MAIS_ESTADOS_AQUI} # Substitua isso pelo restante do seu HTML se tiver mais estados
</ul>
"""
# read from html file
html_content = open('cities.html', 'r', encoding='utf-8').read()

# Substitua {MAIS_ESTADOS_AQUI} pelo restante do seu HTML ou use o HTML completo
# Para este exemplo, vou remover o placeholder para que o código seja executável com o que foi dado.
# html_content = html_content.replace("{MAIS_ESTADOS_AQUI}", "")

# Parse o HTML
soup = BeautifulSoup(html_content, 'html.parser')

# Lista para armazenar os dados extraídos
data = []

# Encontre todos os itens da lista que representam um estado
# Assumindo que a estrutura fornecida é repetida para cada estado dentro de um <ul> pai
state_items = soup.find_all('li', class_='sublist--item', recursive=False) # recursive=False se o <ul> pai for o soup diretamente

# Se o <ul> pai não for o root do 'soup', mas sim o primeiro <ul> encontrado:
if not state_items and soup.find('ul'):
    state_items = soup.find('ul').find_all('li', class_='sublist--item', recursive=False)


for item in state_items:
    # Encontra o link que contém o nome do estado
    state_link = item.find('a', class_='link', attrs={'data-level': '2'})
    if state_link and state_link.find('span'):
        # Pega o nome do estado (o primeiro span dentro do link do estado)
        # É importante pegar o primeiro span para evitar pegar o span do ícone.
        state_name_span = state_link.find('span', recursive=False) # Pega o primeiro span filho direto
        if not state_name_span: # Fallback se o span não for filho direto, mas o primeiro span
             all_spans = state_link.find_all('span')
             if all_spans:
                 state_name_span = all_spans[0]
        
        if state_name_span:
            state_name = state_name_span.get_text(strip=True)

            # Encontra a div que contém a lista de cidades para este estado
            cities_div = item.find('div', class_='sublist--list')
            if cities_div:
                # Dentro dessa div, encontra a lista (ul) de cidades
                cities_ul = cities_div.find('ul', class_='sublist--list')
                if cities_ul:
                    # Encontra todos os itens (li) que representam cidades
                    city_list_items = cities_ul.find_all('li', class_='sublist--item')
                    for city_item in city_list_items:
                        city_link = city_item.find('a', class_='link')
                        # extrair id
                        city_id = city_link['href'].split('=')[-1] if city_link and 'href' in city_link.attrs else None
                        if city_link and city_link.find('span'):
                            city_name = city_link.find('span').get_text(strip=True)
                            data.append({'Cidade': city_name, 'Estado': state_name, 'ID': city_id})

# Crie um DataFrame do Pandas
df = pd.DataFrame(data)
# save the DataFrame to an Excel file
df.to_excel('cities.xlsx', index=False)

# # Exiba o DataFrame
# print("DataFrame Criado:")
# print(df)

# # open other dataframe brasil.xlsx

# df_brasil = pd.read_excel('brasil.xlsx')
# # Merge os DataFrames com base na coluna 'Local' o nome da cidade
# df_merged = pd.merge(df_brasil, df, left_on='Local', right_on='Cidade', how='left')
# # Exiba o DataFrame mesclado    
# print("\nDataFrame Mesclado:")
# print(df_merged)
# # drop the 'Cidade' column from the merged DataFrame
# df_merged.drop(columns=['Cidade'], inplace=True)

# # save the merged DataFrame to a new Excel file
# df_merged.to_excel('brasil2.xlsx', index=False)

# Opcional: Salve o DataFrame em um arquivo CSV
# df.to_csv('cidades_por_estado.csv', index=False)
# print("\nDataFrame salvo como 'cidades_por_estado.csv'")