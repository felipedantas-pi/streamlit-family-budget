import streamlit as st
import pandas as pd

#caminho_planilha = './database/finance2021.xlsx'

nome_subdatasets = ['receitas','despesas','cartões_de_crédito','config']

@st.cache
def load_all_datasets(nome_ou_index = None):
    """ 
    Carrega o conjunto de dados da planhila excel
    como um dicionário de dataframes
    """
    caminho_planilha = './database/finance2021.xlsx'

    return pd.read_excel(caminho_planilha, nome_ou_index) # retorna um dict


@st.cache
def load_dataset():
    """

    """
    df_full = load_all_datasets(nome_ou_index = [0,1,2,3,4])

    receitas = df_full[0].sort_values(by=['DATA']).reset_index(drop=True)
    despesas = df_full[1].sort_values(by=['DATA']).reset_index(drop=True)
    cartoes_de_credito = df_full[2].sort_values(by=['DATA']).reset_index(drop=True)
    
    conf_variable = df_full[3]

    #transacao = df_full[nome_subdatasets[4]].sort_values(by=['DATA']).reset_index(drop=True)

    # função anônima que transforma um str em minúscula
    #lowercase = lambda x: str(x).lower()
    # renomeia as colunas aplicando a função anônima acima
    #conf_variable.rename(lowercase, axis='columns', inplace=True)

    return receitas, despesas, cartoes_de_credito, conf_variable
