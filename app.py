import streamlit as st
from html_app import html_set
html_set() # Carrega o html e configurações da page

from conf import load_all_datasets, load_dataset, nm_banco_cc, categorias_conf

import pandas as pd
from datetime import date
from millify import millify # Converta números longos em um formato legível em Python


#st.write(load_all_datasets())

# Carrega os datasets na memória
receitas, despesas, cartao_credito = load_dataset()[:3] # retorna um dataframe

#Carrega as lista de bancos e cartão de crédito
nm_banco, nm_cartao_credito = nm_banco_cc() # retorna uma lista

# Carrega as listas de bancos, cartões de crédito, 
# categorias de receitas e despesas.
cat_receita, cat_despesa, subcat_despesa = categorias_conf() # retorna uma lista

# Metricas
container1 = st.container()
container1side = st.sidebar.container()
container2side = st.sidebar.container()

## Lista de nomes dos datasets para ser passado a função load_dataset()
#datasets_names = ['','Receitas','Despesas','Cartão de Crédito']
datasets_names = ['receitas', 'despesas', 'cartões de crédito']

meses_nm = ['JAN', 'FEV', 'MAR', 'ABR', 'MAI', 'JUN', 'JUL', 'AGO', 'SET', 'OUT', 'NOV', 'DEZ']
meses_n = list(range(1,13))
# cria um dict {"1":"JAN", "2":"FEV", ...}
meses_dict = {meses_n[i]: meses_nm[i] for i in range(len(meses_n))}

def mes_int2str():
    """
    """
    mes_now = date.today().month # int
    idx = mes_now - 1
    return (mes_now, idx, meses_dict[mes_now]) # returna o valor:str da chave:int


with container1side.expander("FILTRO MENSAL", expanded=True):

    all = st.checkbox("Selecione todos os meses")

    if all:
        meses_options = st.multiselect(
            "Selecione uma mês:", 
            [*meses_dict], #Intera sobre as chaves e retorna uma lista sem precisa do .keys()
            [*meses_dict],
            format_func = lambda m: meses_dict[m])
    else:
        meses_options =  st.selectbox(
            "Selecione uma mês:",
            [*meses_dict], #Intera sobre as chaves e retorna uma lista sem precisa do .keys()
            index = mes_int2str()[1],
            format_func = lambda m: meses_dict[m])

def valor_total_por_mes(dataset:str, mes:int):
    """ 
    Calcula o valor total de um mês de acordo com o dataframe escolhido
    input: nome do dataframe: str, mês: int
    output: numpy.float64
    """
    return dataset[dataset['DATA'].dt.month == mes]['VALOR REAL'].sum() # retorna uma float64


def values_metric(mes:int):
    """
    """
    
    row1, row2, row3 = container1.columns(3)

    nm_mes = meses_dict[mes] # nome do mês Ex: 'JAN'
    mesk_str = {y:x for x,y in meses_dict.items()} # troca key:value 

    recebido = round(valor_total_por_mes(receitas, mesk_str[nm_mes]), 2)
    gastado = round(valor_total_por_mes(despesas, mesk_str[nm_mes]), 2)
    saldo = round(recebido - gastado, 2)

    with row1:
        st.metric('Quanto Recebi', value = recebido)
    with row2:
        st.metric('Quanto Gastei', value = gastado)
    with row3:
        st.metric('Saldo', value = saldo)

## Criando um selectbox para Definindo as opções de dataset
select_dataset = container2side.selectbox(
    label = 'ESCOLHA UM DATASET',
    options = datasets_names,
    index = 0,
    format_func = lambda s: s.title()
)

with st.expander("Filtros de Categorias", expanded = True):

    row1col1, row1col2 = st.columns(2)

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
            with row1col1:
                    
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


