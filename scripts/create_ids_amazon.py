import pandas as pd
import sys


df = pd.read_csv("cities3.csv")


# for each row, create a dictionary with all the columns
cities = []
for index, row in df.iterrows():
    if row["Amazonia"] == "Não":
        continue   
    city = {
        "cidade": row["Cidade"],
        "estado": row["Estado"],
        "id": row["ID"],
    }
    cities.append(city)

# Save the list of cities to a JSON file
import json
with open("cities_amazon.json", "w", encoding="utf-8") as f:
    json.dump(cities, f, ensure_ascii=False, indent=4)

