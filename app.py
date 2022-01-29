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


meses_nm = ['JAN', 'FEV', 'MAR', 'ABR', 'MAI', 'JUN', 'JUL', 'AGO', 'SET', 'OUT', 'NOV', 'DEZ']
meses_n = list(range(1,13))
meses_dict = {meses_nm[i]: meses_n[i] for i in range(len(meses_nm))}


with st.sidebar.expander("FILTRO MENSAL", expanded=True):

    all = st.checkbox("Selecione todos os meses")

    if all:
        meses_options = st.multiselect(
            "Selecione uma mês:", 
            [*meses_nm], #Intera sobre as chaves e retorna uma lista sem precisa do .keys()
            [*meses_nm])
    else:
        meses_options =  st.selectbox(
            "Selecione uma mês:",
            [*meses_nm],
            index=0)


def valor_total_por_mes(dataframe:str, mes:int):
    """ 
    Calcula o valor total de um mês de acordo com o dataframe escolhido
    input: nome do dataframe: str, mês: int
    output: numpy.float64
    """
    return dataframe[dataframe['DATA'].dt.month == mes]['VALOR REAL'].sum() # retorna uma float64


def values_metric(mes:str):
    """
    """
    row1, row2, row3 = container1.columns(3)

    recebido = round(valor_total_por_mes(receitas, meses_dict[meses_options]), 2)
    gastado = round(valor_total_por_mes(despesas, meses_dict[meses_options]), 2)
    saldo = round(recebido - gastado, 2)

    with row1:
        st.metric('Quanto Recebi', value = recebido)
    with row2:
        st.metric('Quanto Gastei', value = gastado)
    with row3:
        st.metric('Saldo', value = saldo)


if all:
    st.markdown(''' ### definir um estado para quando apagar o multiselect ele voltar ao valor padrão que seria o mês atual ''')
    row1, row2, row3 = container1.columns(3)

    recebido = round(receitas['VALOR REAL'].sum(), 2) # 96.871,93
    gastado = round(despesas['VALOR REAL'].sum(), 2) # 97.055,98
    saldo = round(recebido - gastado, 2) # -184,05

    with row1:
        st.metric('Quanto Recebi', value = recebido)
    with row2:
        st.metric('Quanto Gastei', value = gastado)
    with row3:
        st.metric('Saldo', value = saldo)


if meses_options == 'JAN':
    values_metric(meses_options)

if meses_options == 'FEV':
    values_metric(meses_options)

if meses_options == 'MAR':
    values_metric(meses_options)

if meses_options == 'ABR':
    values_metric(meses_options)

if meses_options == 'MAI':
    values_metric(meses_options)

if meses_options == 'JUN':
    values_metric(meses_options)

if meses_options == 'JUL':
    values_metric(meses_options)

if meses_options == 'AGO':
    values_metric(meses_options)

if meses_options == 'SET':
    values_metric(meses_options)

if meses_options == 'OUT':
    values_metric(meses_options)

if meses_options == 'NOV':
    values_metric(meses_options)

if meses_options == 'DEZ':
    values_metric(meses_options)

