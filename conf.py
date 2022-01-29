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


@st.cache
def nm_banco_cc():

    # Carrega o dataset com a configuração de Bancos e Cartão de Crédito
    df = load_dataset()[3]

    # Seleciona a coluna de banco e criar um lista de valores
    banco_name = df['Bancos'].dropna().tolist()

    # Seleciona a colina de Cartão de Crédito e exporta para lista
    cardCredit_name = df['Cartão de Crédito'].dropna().tolist()

    return banco_name, cardCredit_name


@st.cache
def categorias_conf():

    # Carrega o dataset com a configuração de despesas
    df = load_dataset()[3]

    # Obtem a lista de categorias das receitas
    cat_receitas = sorted(df['Receita'].dropna().tolist())

    # Obtem a lista de categorais das despesas
    cat_despesa = sorted(df['Despesa'].dropna().tolist())
    # Gera um lista de despesas pelos nomes das colunas das subdespesas
    #cat_despesa = df.columns.tolist()[3:]

    # Inicializa com um dicionário vázio
    subcat_despesa = {}

    # Aqui utilizo um dictionary comprehension para adicionar 
    # as Keys com os nomes do cabeçalho do dataframe
    # e criar um lista de subcategorias por categoria
    subcat_despesa = {new_list: None for new_list in cat_despesa}

    # Aqui 
    for c in cat_despesa:
        subcat_despesa[c] = df[c].dropna().tolist()
    
    return cat_receitas, cat_despesa, subcat_despesa