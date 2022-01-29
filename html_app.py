import streamlit as st

# Usando HTML para renderizar o título
# Esconde o icône de hamburgue do streamlit
def html_set():
    padding = 0
    title_html = """
    <style>
        // esconde o icon do streamlit
        #MainMenu {visibility: hidden;}

        // esconde o footer streamlit
        footer {visibility: hidden;}

        //
        .reportview-container .main .block-container{{
            padding-top: {padding}rem;
            padding-right: {padding}rem;
            padding-left: {padding}rem;
            padding-bottom: {padding}rem;
        }}

        .title{
            margin:0;
            padding: 0;
        }

        .title h1{
            text-align: center;
            padding: 0px;
        }

        .title h2{
            text-align:center;
            padding: 0px;
        }

        .title-autor h3{
            text-align:center;
            margin-top: 10px;
            padding: 0px;
            font-size: 10px;
        }
    </style> 
    
    <div class="title">
        <h1>ORÇAMENTO FAMILIAR</h1>
        <h2>2022</h2>
    </div>
    <div class="title-autor">
        <h3>Autor: Felipe Dantas</h3>
    </div>
    """

    return st.sidebar.markdown(title_html, unsafe_allow_html=True)