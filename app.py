import streamlit as st

st.set_page_config(
    page_title = 'Finanças Familiar',
    page_icon = "🖖",
    layout ="wide",
    initial_sidebar_state = "collapsed",
    menu_items =    {
        'Get Help': '',
        'Report a bug': "h",
        'About': "# This is a header. This is an *extremely* cool app!"})

from html_app import html_set
html_set() # Carrega o html 

from conf import load_all_datasets, load_dataset, nm_banco_cc, categorias_conf

import pandas as pd
import numpy as np
from datetime import date
from millify import millify # Converta números longos em um formato legível em Python


#st.write(load_all_datasets())

# Carrega os dataframe datasets
receitas, despesas, cartao_credito = load_dataset()[:3] # retorna um dataframe

#Carrega as lista de bancos e cartão de crédito
nm_banco, nm_cartao_credito = nm_banco_cc() # retorna uma lista

# Carrega as listas de bancos, cartões de crédito, 
# categorias de receitas e despesas.
cat_receita, cat_despesa, subcat_despesa = categorias_conf() # retorna uma lista

#subcat_despesa['Alimentação']

# Metricas
container1 = st.container()

def valor_total_por_mes(dataframe:str, mes:int):
    """ 
    Calcula o valor total de um mês de acordo com o dataframe escolhido
    input: nome do dataframe: str, mês: int
    output: numpy.float64
    """
    return dataframe[dataframe['DATA'].dt.month == mes]['VALOR REAL'].sum() # retorna uma float64

## Lista de nomes dos datasets para ser passado a função load_dataset()
#datasets_names = ['','Receitas','Despesas','Cartão de Crédito']
datasets_names = ['receitas','despesas','cartões de crédito']

## Criando um selectbox para Definindo as opções de dataset
select_dataset = st.sidebar.selectbox(
  label = 'ESCOLHA UM DATASET',
  options = datasets_names,
  index = 0,
  format_func = lambda s: s.title()
)


with st.expander("Filtros de Categorias", expanded = True):

    row1col1, row1col2, row1col3 = st.columns(3)
    ## Habilita as caixas de seleções de acordo com o dataset escolhido
    if select_dataset == datasets_names[0]: # Receitas
        with row1col1:

            options_bank = st.multiselect(
                label = 'Conta bancária',
                options = nm_banco,
                default = None
            )

        with row1col2:

            options_cat_receitas = st.multiselect(
                label = 'Categorias de Receitas',
                options = cat_receita,
                #options = receitas['FONTE DE RENDA'].unique(),
                default = None
            )

    elif select_dataset == datasets_names[1]: # Despesas
        with row1col1:

            options_bank = st.multiselect(
                label = 'Conta bancária',
                options = nm_banco,
                default = None
            )

        with row1col2:

            options_despesa = st.selectbox(
                label = 'Categoria de Despesa',
                options = [''] + sorted(cat_despesa),
                #default = None,
                key='name_cat_despesa'
            )

        if len(options_despesa) > 0:
            with row1col3:
                    
                 options_subdespesa = st.selectbox(
                    "Subcategoria da despesa selecionada",
                    options = subcat_despesa[options_despesa],
                    #default = None
                )

    elif select_dataset == datasets_names[2]: # Cartão de Crédito
        # colocar aqui informações do cartao de credito que usara, 
        # provavelmente 3 colunas
        pass
    else:
        # colocar aqui um dashboar geral ou não
        pass


