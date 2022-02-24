from html_app import html_set
html_set() # Carrega o html e configurações da page

import streamlit as st
import pandas as pd
from datetime import date
from millify import millify # Converta números longos em um formato legível em Python

from conf import load_all_datasets, load_dataset, nm_banco_cc, categorias_conf
from func import dict_mes, mes_int2str, valor_total_por_mes

import seaborn as sns
import matplotlib.pyplot as plt
#sns.set_theme(style="ticks", color_codes=True)
#import plots

receitas, despesas, cartao_credito = load_dataset()[:3] # retorna um dataframe
nm_banco, nm_cartao_credito = nm_banco_cc() # retorna uma lista
cat_receita, cat_despesa, subcat_despesa = categorias_conf() # retorna uma lista

# Metricas
container1 = st.container()
container2 = st.container()
container3 = st.container()

# Sidebar
container1side = st.sidebar.container()
container2side = st.sidebar.container()

#meses_nm = ['JAN', 'FEV', 'MAR', 'ABR', 'MAI', 'JUN', 'JUL', 'AGO', 'SET', 'OUT', 'NOV', 'DEZ']
#meses_n = list(range(1,13))
#meses_dict = {meses_n[i]: meses_nm[i] for i in range(len(meses_n))} # dict {"1":"JAN", ...}

# CRIANDO FILTROS

## Temporal
with container1side.expander("FILTRO MENSAL", expanded=True):

    all = st.checkbox("Selecione todos os meses")

    if all:
        meses_options = st.multiselect(
            "Selecione uma mês:", 
            [*dict_mes()], #Intera sobre as chaves e retorna uma lista sem precisa do .keys()
            [*dict_mes()],
            format_func = lambda m: dict_mes()[m])
    else:
        meses_options =  st.selectbox(
            "Selecione uma mês:",
            [*dict_mes()], #Intera sobre as chaves e retorna uma lista sem precisa do .keys()
            index = mes_int2str()[0] - 1,
            format_func = lambda m: dict_mes()[m])

## Datasets
datasets_names = ['receitas', 'despesas', 'cartões de crédito']

select_dataset = container2side.selectbox(
    label = 'ESCOLHA UM DATASET',
    options = datasets_names,
    index = 0,
    format_func = lambda s: s.title())

## Filtros de acordo com o dataset selecionado
with container2.expander("Filtros de Categorias", expanded = True):

    row1col1, row1col2 = st.columns(2)

    if select_dataset == datasets_names[0]: # receitas
        with row1col1:

            options_bank = st.multiselect(
                label = 'Contas bancárias',
                options = nm_banco,
                default = None
            )
        
        filter_bank = receitas['CONTA'].isin(options_bank)
        receita_filter_bank = receitas.loc[:, filter_bank]
        st.dataframe(receita_filter_bank)
        

        with row1col2:

            options_cat_receitas = st.multiselect(
                label = 'Categorias de Receitas',
                options = cat_receita,
                #options = receitas['FONTE DE RENDA'].unique(),
                default = None
            )

    elif select_dataset == datasets_names[1]: # despesas
        with row1col1:

            options_bank = st.multiselect(
                label = 'Conta bancária',
                options = nm_banco,
                default = None
            )

        with row1col2:

            options_cat_despesas = st.selectbox(
                label = 'Categoria de Despesa',
                options = [''] + sorted(cat_despesa),
                #default = None,
                key='name_cat_despesa'
            )

            if len(options_cat_despesas) > 0:
                with row1col2:
                        
                    options_subcat_despesas = st.selectbox(
                        "Subcategoria da despesa selecionada",
                        options = subcat_despesa[options_cat_despesas],
                        #default = None
                    )

    elif select_dataset == datasets_names[2]: # cartão de credito
        st.warning("Implementado em andamento")
        # colocar aqui informações do cartao de credito que usara, 
        # provavelmente 3 colunas
        pass
    else:
        # colocar aqui um dashboar geral ou não
        pass

def values_metric(mes:int):
    """
    """
    row1, row2, row3 = container1.columns(3)

    nm_mes = dict_mes()[mes] # Valor da key: 'JAN' 
    mesk_str = {y:x for x,y in dict_mes().items()} # troca key:value 

    recebido = round(valor_total_por_mes(receitas, mesk_str[nm_mes])[1], 2) 
    gastado = round(valor_total_por_mes(despesas, mesk_str[nm_mes])[1], 2)
    saldo = round(recebido - gastado, 2)

    with row1:
        st.metric('Quanto Recebi', value = recebido)
    with row2:
        st.metric('Quanto Gastei', value = gastado)
    with row3:
        st.metric('Saldo', value = saldo)

    st.dataframe(valor_total_por_mes(receitas, mesk_str[nm_mes])[0])


# Criar o container1 com os valores recebidos, gastados e saldo
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
else:
    values_metric(meses_options)





# f1 = (receitas['CONTA'].isin(options_bank))
# f2 = (receitas['FONTE DE RENDA'].isin(options_categorias_receitas))
# receitas.loc(filter1)

# f1 = (receitas["DATA"] >= pd.to_datetime(start_date)) & (receitas["DATA"] <= pd.to_datetime(end_date))
# f2 = (receitas['CONTA'].isin(options_bank))
# f3 = (receitas['FONTE DE RENDA'].isin(options_categorias_receitas))