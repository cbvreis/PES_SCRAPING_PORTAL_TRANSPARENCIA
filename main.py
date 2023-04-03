import requests as re
import pandas as pd

#Letras alfabeto como uma lista
alfabeto = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")



def main():
    json = re.get(f"https://portaldatransparencia.gov.br/pessoa-juridica/busca/resultado?pagina=1&tamanhoPagina=10000&ufPessoaJuridica=SP&municipio=3509502&").json()
    df = pd.DataFrame(json["registros"])
    #criar uma coluna de URL seguindo exemplo:
    ##NOME: A AZEVEDO INDUSTRIA E COMERCIO DE OLEOS LTDA
    ##CNPJ: 61278875000306
    ##URL: https://portaldatransparencia.gov.br/busca/pessoa-juridica/61278875000306-a-azevedo-industria-e-comercio-de-oleos-ltda
    df["URL"] = df.apply(lambda x: f"https://portaldatransparencia.gov.br/busca/pessoa-juridica/{x['cnpj']}-{x['nome'].lower().replace(' ', '-')}", axis=1)

    #Substituir & por and
    df["URL"] = df["URL"].apply(lambda x: x.replace("&", "and"))

    df.to_excel(f"campinas.xlsx", index=False)


if __name__ == "__main__":

    main()
