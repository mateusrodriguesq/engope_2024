import pandas as pd
import numpy as np
import openpyxl

def import_database():
    #importando a base de dados in data/dados_escores.xlsx converting these to float: Altura	EstDesenv	Invasoras	Cupins	CobertSolo	DispForr	DispFolhVerd	CondAtual	PotProd	Degrad	Manejo

    #dados_scores = pd.read_excel('data/dados_escores.xlsx')
    #importando a base de dados in data/dados_geoloc_classe.xlsx
    #dados_geoloc_classe = pd.read_excel('data/dados_geoloc_classe.xlsx')
    #importando a base de dados in data/dicionario_variaveis.xlsx
    #dicionario_variaveis = pd.read_excel('data/dicionario_variaveis.xlsx')

    #dados_scores.to_parquet('data/dados_scores.parquet')
    #dados_geoloc_classe.to_parquet('data/dados_geoloc_classe.parquet')
    #dicionario_variaveis.to_parquet('data/dicionario_variaveis.parquet')

    #read parquet
    dados_scores = pd.read_parquet('data/dados_scores.parquet')
    dados_geoloc_classe = pd.read_parquet('data/dados_geoloc_classe.parquet')
    dicionario_variaveis = pd.read_parquet('data/dicionario_variaveis.parquet')


    return dados_scores, dados_geoloc_classe, dicionario_variaveis


class import_db:
    #save the databases in the class as dataframes to be used in the app
    def __init__(self):
        self.dados_scores, self.dados_geoloc_classe, self.dicionario_variaveis = import_database()

    def get_dados_scores(self):
        #convert to dataframe
        self.dados_scores = pd.DataFrame(self.dados_scores)
        return self.dados_scores

    def get_dados_geoloc_classe(self):
        #convert to dataframe
        self.dados_geoloc_classe = pd.DataFrame(self.dados_geoloc_classe)
        return self.dados_geoloc_classe

    def get_dicionario_variaveis(self):
        #convert to dataframe
        self.dicionario_variaveis = pd.DataFrame(self.dicionario_variaveis)
        return self.dicionario_variaveis

