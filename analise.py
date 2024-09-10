# %%
import pandas as pd
from IPython.display import display
import plotly.express as px
import plotly.express as px

# %%
def load_data():
    alunos = pd.read_json('aluno.json')
    matricula = pd.read_json('MatriculaPeriodo.json')
    notas = pd.read_json('Notas.json')
    disciplina = pd.read_json('Disciplina.json')
    situacao = pd.read_json('SituacaoMatriculaPeriodo.json')

    return alunos, matricula, notas, disciplina, situacao

#  %%
def main():
    alunos, matricula, notas, disciplina, situacao = load_data()
    
    display(alunos.head())
    display(matricula.head())
    display(notas.head())
    display(disciplina.head())
    display(situacao.head())

    # df_merged = pd.merge(alunos, matricula, left_on='id', right_on='aluno_id', suffixes=('_aluno', '_matricula'))
    # display(df_merged)

    merge_matricula_situacao = pd.merge(matricula, situacao, left_on='situacao_id', right_on='id', suffixes=('_matricula', '_situacao'))
    display(merge_matricula_situacao)
    #print("Merge matricula -> situacao")
    #display(merge_matricula_situacao)

    merge_matricula_situacao_notas = pd.merge(notas, merge_matricula_situacao, left_on='matricula_periodo_id', right_on='id_matricula', suffixes=('', '_notas'))
    
    #print("Notas -> Merge matricula situacao ")
    #display(merge_matricula_situacao_notas)

    # Merge 
    merge_matricula_situacao_notas_disciplina = pd.merge(merge_matricula_situacao_notas, disciplina, left_on='disciplina_id', right_on='id', suffixes=('', '_disciplina'))
    
    #print("Disciplina -> Merge matricula situacao notas ")
    display(merge_matricula_situacao_notas_disciplina)

    merge_matricula_situacao_notas_disciplina_alunos = pd.merge(merge_matricula_situacao_notas_disciplina, alunos, left_on='aluno_id', right_on='id', suffixes=('', '_aluno'))

    filter_df = merge_matricula_situacao_notas_disciplina_alunos[merge_matricula_situacao_notas_disciplina_alunos['descricao_historico'].str.startswith('Matematica I')]

    filter_df_final = filter_df.dropna(subset=['professores'])

    display(filter_df_final)

    #display(filter_df_final[["id_matricula","descricao_historico", "ch_hora_relogio", "media_final", "percentual_frequencia"]])
    #display(filter_df_final)
    #display(filter_df_final[['percentual_frequencia', 'media_final']])
    #display(filter_df_final[['professores','media_final']])



    # Criando o gráfico de dispersão interativo
    fig = px.scatter(
        filter_df_final, 
        x='media_final', 
        y='percentual_frequencia', 
        text='descricao_historico',  # Adiciona os rótulos das disciplinas
        title='Relação entre Média Final e Percentual de Frequência',
        labels={'media_final': 'Média Final', 'percentual_frequencia': 'Percentual de Frequência'},
        template='plotly_white'
    )

    # Ajustando a posição dos rótulos para não sobrepor os pontos
    # fig.update_traces(textposition='top center')
    
    # display.plotly_chart(fig)


if __name__ == "__main__":
    main()
#  %%