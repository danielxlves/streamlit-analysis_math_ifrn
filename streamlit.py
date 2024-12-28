import streamlit as st
import pandas as pd
import joblib
from catboost import CatBoostClassifier
import numpy as np

# Carregando o modelo e os encoders
model = joblib.load('./modelo_predicao_reprovacao_bestmodel.pkl')
encoders = joblib.load('./encoders.pkl')

# Mapeamentos para variáveis categóricas
mapeamentos = {
    'descricao_historico': {0: 'Arte I(30H)', 1: 'Arte II(30H)', 2: 'Arte III(30H)', 3: 'Biologia I(90H)',
                            4: 'Biologia II(120H)', 5: 'Educação Física I(60H)', 6: 'Educação Física II(60H)',
                            7: 'Filosofia I(30H)', 8: 'Filosofia II(30H)', 9: 'Física I(120H)',
                            10: 'Física II(120H)', 11: 'Geografia I(120H)', 12: 'Geografia II(60H)',
                            13: 'História I(60H)', 14: 'História II(120H)', 15: 'Língua Portuguesa e Literatura I(90H)',
                            16: 'Língua Portuguesa e Literatura II(90H)', 17: 'Língua Portuguesa e Literatura III(90H)',
                            18: 'Matematica I(120H)', 19: 'Matematica II(90H)', 20: 'Matematica III(90H)',
                            21: 'Química I(120H)', 22: 'Química II(120H)', 23: 'Sociologia I(30H)',
                            24: 'Sociologia II(30H)', 25: 'Sociologia III(30H)'},
    'carga_horaria_categoria': {0: 'Alta', 1: 'Baixa', 2: 'Média'},
    'campo_disciplinar': {0: 'Biológicas', 1: 'Exatas', 2: 'Humanas'}
}

# Mapeamento das disciplinas para seus respectivos campos
campo_disciplinar_map = {
    'Geografia I(120H)': 'Humanas',
    'Geografia II(60H)': 'Humanas',
    'Filosofia I(30H)': 'Humanas',
    'Filosofia II(30H)': 'Humanas',
    'Sociologia I(30H)': 'Humanas',
    'Sociologia II(30H)': 'Humanas',
    'Sociologia III(30H)': 'Humanas',
    'História I(60H)': 'Humanas',
    'História II(120H)': 'Humanas',
    'Arte I(30H)': 'Humanas',
    'Arte II(30H)': 'Humanas',
    'Arte III(30H)': 'Humanas',
    'Língua Portuguesa e Literatura I(90H)': 'Humanas',
    'Língua Portuguesa e Literatura II(90H)': 'Humanas',
    'Língua Portuguesa e Literatura III(90H)': 'Humanas',
    'Educação Física I(60H)': 'Humanas',
    'Educação Física II(60H)': 'Humanas',
    'Matematica I(120H)': 'Exatas',
    'Matematica II(90H)': 'Exatas',
    'Matematica III(90H)': 'Exatas',
    'Física I(120H)': 'Exatas',
    'Física II(120H)': 'Exatas',
    'Química I(120H)': 'Exatas',
    'Química II(120H)': 'Exatas',
    'Biologia I(90H)': 'Biológicas',
    'Biologia II(120H)': 'Biológicas',
}

# Invertendo os mapeamentos para facilitar a busca posterior
inverse_mapeamentos = {key: {v: k for k, v in value.items()} for key, value in mapeamentos.items()}

# Função para realizar a codificação e previsão
def predict(input_data):
    # Convertendo os dados de entrada para o formato de DataFrame
    input_df = pd.DataFrame([input_data], columns=['descricao_historico', 'num_professores', 'percentual_frequencia', 
                                                   'carga_horaria_categoria', 'campo_disciplinar', 'media_campo_disciplinar'])

    # Mapear a disciplina para o campo disciplinar
    campo_disciplinar = campo_disciplinar_map.get(input_data['descricao_historico'], 'Humanas')
    input_df['campo_disciplinar'] = campo_disciplinar

    # Codificando as variáveis categóricas com os mapeamentos
    for col in ['descricao_historico', 'carga_horaria_categoria', 'campo_disciplinar']:
        input_df[col] = input_df[col].map(inverse_mapeamentos[col])

    st.write("DataFrame input_df como JSON:")
    st.json(input_df.to_dict())

    # Obtendo as probabilidades com o modelo
    probabilidade = model.predict_proba(input_df)
    
    return probabilidade

# Interface Streamlit
st.title("Previsão de Reprovação")

# Campos de entrada
descricao_historico = st.selectbox('Descrição do Histórico', list(campo_disciplinar_map.keys()))

# Atualizando o campo disciplinar com base na escolha da disciplina
campo_disciplinar = campo_disciplinar_map.get(descricao_historico, 'Humanas')  # Valor padrão como 'Humanas'

# Exibindo o campo disciplinar automaticamente
st.write(f'Campo Disciplinar: {campo_disciplinar}')

# Outros campos para a previsão (exemplos)
num_professores = st.number_input('Número de Professores', min_value=1, max_value=10, value=5)
percentual_frequencia = st.slider('Percentual de Frequência', 0, 100, 75)
carga_horaria_categoria = st.selectbox('Categoria de Carga Horária', ['Alta', 'Média', 'Baixa'])
media_campo_disciplinar = st.number_input('Média do Campo Disciplinar', min_value=0.0, max_value=10.0, value=7.0)

# Preparando os dados para a previsão
input_data = {
    'descricao_historico': descricao_historico,
    'num_professores': num_professores,
    'percentual_frequencia': percentual_frequencia,
    'carga_horaria_categoria': carga_horaria_categoria,
    'campo_disciplinar': campo_disciplinar,
    'media_campo_disciplinar': media_campo_disciplinar
}

# Botão para fazer a previsão
if st.button('Prever'):
    probabilidade = predict(input_data)
    st.write(f'Probabilidade de Reprovação: {probabilidade[0][1]:.2f}')
