import streamlit as st
import pandas as pd
import io
import plotly.express as px

def load_data():
    dados_mergado = pd.read_json('dados_workflow_ivan.json')
    return dados_mergado

def main():
    dados_mergado = load_data()
    matematica_i = dados_mergado["MatemticaI120H"].dropna()

    st.title('Análise de dados da disciplina \"Matemática I\" dos cursos integrados do IFRN.')

    buffer = io.StringIO()
    dados_mergado.info(buf=buffer)
    s = buffer.getvalue()
    st.code("Informações do dataset com os dados combinados:\n" + s)

    st.header('Series da disciplina de \"Matemática I\", filtrada dos dados combinados.')    
    st.dataframe(matematica_i)
    
    fig = px.histogram(matematica_i, x=matematica_i, title='Distribuição de Notas em Matemática I')
    st.plotly_chart(fig)
        
if __name__ == "__main__":
    main()
