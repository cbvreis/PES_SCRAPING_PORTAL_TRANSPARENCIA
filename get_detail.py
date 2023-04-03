import time
import pandas as pd
import requests as re
from selenium import webdriver
from bs4 import BeautifulSoup
from multiprocessing import Pool

# Definir o número de processos a serem executados simultaneamente
NUM_PROCESSOS = 4

#Instanciar o webdriver
#driver = webdriver.Chrome('chromedriver.exe')

#Ler o arquivo pandas com as URLs
df = pd.read_excel("campinas.xlsx")


def write_file_append(data, file_name):
    with open(file_name, 'a') as f:
        f.write(str(data) + '\n')


def get_data(url):
#i=0
#list_df = []
#for url in df["URL"]:
    try:
        driver = webdriver.Chrome('chromedriver.exe')

        # encontrar os elementos HTML que contêm as informações desejadas
        driver.get(url)
        print('Aguardando 5 segundos para carregar a página')
        time.sleep(2)

        # Extrai o HTML da página resultante
        html = driver.page_source

        # Cria o objeto BeautifulSoup
        soup = BeautifulSoup(html, "html.parser")

        #
        container = soup.find("section", {"class": "dados-tabelados"})

        # Encontra as informações desejadas dentro do container
        cnpj = container.find("strong", text="Número de inscrição").find_next_sibling("span").text.strip()
        abertura = container.find("strong", text="Data de abertura").find_next_sibling("span").text.strip()
        email = container.find("strong", text="Endereço eletrônico").find_next_sibling("span").text.strip()
        telefone = container.find("strong", text="Telefone").find_next_sibling("span").text.strip()
        nome_empresarial = container.find("strong", text="Nome empresarial").find_next_sibling("span").text.strip()
        nome_fantasia = container.find("strong", text="Nome de fantasia").find_next_sibling("span").text.strip()
        natureza_juridica = container.find("strong", text="Natureza jurídica").find_next_sibling("span").text.strip()
        cnae = container.find("strong", text="CNAE").find_next_sibling("span").text.strip()
        logradouro = container.find("strong", text="Logradouro").find_next_sibling("span").text.strip()
        numero = container.find("strong", text="Número").find_next_sibling("span").text.strip()
        complemento = container.find("strong", text="Complemento").find_next_sibling("span").text.strip()
        cep = container.find("strong", text="CEP").find_next_sibling("span").text.strip()
        bairro = container.find("strong", text="Bairro/Distrito").find_next_sibling("span").text.strip()
        municipio = container.find("strong", text="Município").find_next_sibling("span").text.strip()
        uf = container.find("strong", text="UF").find_next_sibling("span").text.strip()

        # Cria um dataframe com as informações
        df = pd.DataFrame({
            "URL": [url],
            "CNPJ": [cnpj],
            "Data de Abertura": [abertura],
            "Email": [email],
            "Telefone": [telefone],
            "Nome Empresarial": [nome_empresarial],
            "Nome Fantasia": [nome_fantasia],
            "Natureza Jurídica": [natureza_juridica],
            "CNAE": [cnae],
            "Logradouro": [logradouro],
            "Número": [numero],
            "Complemento": [complemento],
            "CEP": [cep],
            "Bairro": [bairro],
            "Município": [municipio],
            "UF": [uf]
        })

        write_file_append(df.to_dict('records'), 'campinas_detalhes.txt')
        driver.quit()
        return df
    except Exception as e:
        print(e)
        print(f"Erro na URL: {url}")
        pass

if __name__ == '__main__':
    # Define o número de processos que serão executados simultaneamente
    pool = Pool(processes=NUM_PROCESSOS)

    # Executa a função get_data em cada URL
    list_df = pool.map(get_data, df["URL"])

    # Concatena os dataframes em um único dataframe
    df_final = pd.concat(list_df)

    # Salva o dataframe em um arquivo Excel
    df_final.to_excel("campinas_detalhes.xlsx", index=False)


