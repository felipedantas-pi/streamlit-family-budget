def dict_mes():
    
    meses_nm = ['JAN', 'FEV', 'MAR', 'ABR', 'MAI', 'JUN', 'JUL', 'AGO', 'SET', 'OUT', 'NOV', 'DEZ']
    meses_n = list(range(1,13))
    meses_dict = {meses_n[i]: meses_nm[i] for i in range(len(meses_n))} # dict {"1":"JAN", ...}

    return meses_dict



def mes_int2str():

    from datetime import date
    num_mes_now = date.today().month # int

    return (num_mes_now, dict_mes()[num_mes_now])


def valor_total_por_mes(dataset, mes:int, **columns_df):
    """ 
    Calcula o valor total de um mês de acordo com o dataframe escolhido
    input: nome do dataframe: str, mês: int
    output: numpy.float64
    """
    import streamlit as st
    import pandas as pd

    bank_selected = columns_df.get('bank')
    cat_receita_sel = columns_df.get('categoria_receita')

    if mes is None:
        st.write("Nenhum mes especificado")
        receita_contas = dataset.loc[dataset['CONTA'].isin(bank_selected)]
    else:
        df = dataset[dataset['DATA'].dt.month == mes] # dados do mes selecionado
        mes_soma = df['VALOR REAL'].sum() # somatório

    return df, mes_soma # retorna uma float64


receita_contas
receita_contas.loc[receita_contas['FONTE DE RENDA'].isin(options_cat_receitas)]

# f1 = (receitas["DATA"] >= pd.to_datetime(start_date)) & (receitas["DATA"] <= pd.to_datetime(end_date))
# f2 = (receitas['CONTA'].isin(options_bank))
# f3 = (receitas['FONTE DE RENDA'].isin(options_categorias_receitas))



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


