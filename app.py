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


