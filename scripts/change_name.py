import pandas as pd

df = pd.read_csv('brasil4.csv')

# apply change to column Local if match pattern ' (Município)' remove it
df['Local'] = df['Local'].str.replace(r'\s*\(Município\)$', '', regex=True).str.strip()

# save brasil 5 
df.to_csv('brasil5.csv', index=False)