import pandas as pd

df = pd.read_csv('cities6.csv')

# convert all values - to blank
df = df.replace('-', '')

# save the modified DataFrame to a new CSV file
df.to_csv('cities6.csv', index=False)