
import streamlit as st
import pandas as pd
import io
import plotly.express as px

def load_data():
    #alunos = pd.read_json('aluno.json')
    matricula = pd.read_json('MatriculaPeriodo.json')
    notas = pd.read_json('Notas.json')
    disciplina = pd.read_json('Disciplina.json')
    situacao = pd.read_json('SituacaoMatriculaPeriodo.json')

    return matricula, notas, disciplina, situacao

def main():

    matricula, notas, disciplina, situacao = load_data()

    #st.text("Aluno")
    #st.dataframe(alunos)
    #st.text("Matricula")
    #st.dataframe(matricula)
    #st.text("Notas")
    #st.dataframe(notas)
    #st.text("Disciplinas")
    #st.dataframe(disciplina)
    #st.text("Situacao")
    #st.dataframe(situacao)

    # Merges/Joins

    merge_matricula_situacao = pd.merge(matricula, situacao, left_on='situacao_id', right_on='id', suffixes=('_matricula', '_situacao'))
    
    st.text("Merge matricula -> situacao")
    
    st.dataframe(merge_matricula_situacao)

    merge_matricula_situacao_notas = pd.merge(notas, merge_matricula_situacao, left_on='situacao_id', right_on='id_situacao', suffixes=('', '_notas'))
    
    #Merge final
    merge_matricula_situacao_notas_disciplina = pd.merge(merge_matricula_situacao_notas, disciplina, left_on='situacao_id', right_on='id', suffixes=('', '_disciplina'))

    #st.dataframe(merge_matricula_situacao_notas_disciplina)

if __name__ == "__main__":
    main()


