import re
import pandas as pd

# Define o padrão de expressão regular para extrair os dados
pattern = r"\{(?:\s*\'.*?\':\s*\'.*?\',?)*\}"

# Cria uma lista vazia para armazenar os dicionários de dados
data = []

# Abre o arquivo e lê as linhas
with open("campinas_detalhes.text", "r") as f:
    lines = f.readlines()

    # Itera pelas linhas e extrai os dicionários de dados usando o padrão de expressão regular
    for line in lines:
        match = re.search(pattern, line)
        if match:
            data.append(eval(match.group()))

# Cria o DataFrame Pandas a partir da lista de dicionários de dados
df = pd.DataFrame(data) 


df.to_excel("campinas_detalhes.xlsx", index=True)