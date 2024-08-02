import streamlit as st
import pandas as pd
import io

def load_data():
    disciplina_df = pd.read_json('Disciplina.json')
    matricula_periodo_df = pd.read_json('MatriculaPeriodo.json')
    notas_df = pd.read_json('Notas.json')
    situacao_matricula_periodo_df = pd.read_json('SituacaoMatriculaPeriodo.json')
    
    return disciplina_df, matricula_periodo_df, notas_df, situacao_matricula_periodo_df

def main():
    st.title('Análise de dados das disciplinas de matematica (i, ii, iii) dos cursos integrados do IFRN.')
    
    disciplina_df, matricula_periodo_df, notas_df, situacao_matricula_periodo_df = load_data()
    
    st.header('Disciplina.json')
    st.write(disciplina_df.head(2))
    
    st.header('MatriculaPeriodo.json')
    st.write(matricula_periodo_df.head(2))
    
    st.header('Notas.json')
    st.write(notas_df.head(2))
    
    st.header('SituacaoMatriculaPeriodo.json')
    st.write(situacao_matricula_periodo_df.head(2))

    option = st.selectbox(
        'Escolha um dataset para explorar:',
        ['Disciplina', 'MatriculaPeriodo', 'Notas', 'SituacaoMatriculaPeriodo']
    )
    
    if option == 'Disciplina':
        st.dataframe(disciplina_df)
        buffer = io.StringIO()
        disciplina_df.info(buf=buffer)
        s = buffer.getvalue()
        st.code("Informações do dataset 'Disciplina':\n" + s)
    elif option == 'MatriculaPeriodo':
        st.dataframe(matricula_periodo_df)
        buffer = io.StringIO()
        matricula_periodo_df.info(buf=buffer)
        s = buffer.getvalue()
        st.code("Informações do dataset 'MatriculaPeriodo':\n" + s)
    elif option == 'Notas':
        st.dataframe(notas_df)
        buffer = io.StringIO()
        notas_df.info(buf=buffer)
        s = buffer.getvalue()
        st.code("Informações do dataset 'Notas':\n" + s)
    elif option == 'SituacaoMatriculaPeriodo':
        st.dataframe(situacao_matricula_periodo_df)
        buffer = io.StringIO()
        situacao_matricula_periodo_df.info(buf=buffer)
        s = buffer.getvalue()
        st.code("Informações do dataset 'SituacaoMatriculaPeriodo':\n" + s)
        
if __name__ == "__main__":
    main()
