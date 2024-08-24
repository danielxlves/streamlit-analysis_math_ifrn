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

    #print("Aluno")
    #print(alunos)
    #print("Matricula")
    #print(matricula)
    #print("Notas")
    #print(notas)
    #print("Disciplinas")
    #print(disciplina)
    #print("Situacao")
    #print(situacao)

    # Merges/Joins

    merge_matricula_situacao = pd.merge(matricula, situacao, left_on='situacao_id', right_on='id', suffixes=('_matricula', '_situacao'))
    
    print("Merge matricula -> situacao")
    print(merge_matricula_situacao)

    merge_matricula_situacao_notas = pd.merge(notas, merge_matricula_situacao, left_on='situacao_id', right_on='id_situacao', suffixes=('', '_notas'))
    
    print("Notas -> Merge matricula situacao ")
    print(merge_matricula_situacao_notas)
    

    #Merge final
    merge_matricula_situacao_notas_disciplina = pd.merge(merge_matricula_situacao_notas, disciplina, left_on='situacao_id', right_on='id', suffixes=('', '_disciplina'))
    
    print("Disciplina -> Merge matricula situacao notas ")
    print(merge_matricula_situacao_notas_disciplina)

if __name__ == "__main__":
    main()





# %%
