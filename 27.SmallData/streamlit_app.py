import streamlit as st
import duckdb
import pandas as pd
import plotly.express as px

#dados
con = duckdb.connect('data/db.duckdb', read_only=True)
alunos_df = con.execute("SELECT * FROM alunos").fetchdf()
con.close()

st.title("Alunos")

st.sidebar.header('Configurações do Filtro')
alunos_selecionados = st.sidebar.multiselect(
    'Selecione um aluno',
    options=alunos_df['nome'].unique(),
    default=alunos_df['nome'].unique()
)

st.sidebar.info("Use os filtros acima para ajustar os dados e a visualização.")

dados_filtrados = alunos_df[alunos_df['nome'].isin(alunos_selecionados)]
dados_filtrados = dados_filtrados.sort_values('nome', ascending=False)

tab1, tab2 = st.tabs(["Dados", "Gráfico"])

with tab1:
    st.write(dados_filtrados)

if not dados_filtrados.empty:
    with tab2:
        fig = px.bar(
            dados_filtrados,
            x='nome',
            y='nome',
            orientation='h',
            title='Contagem de alunos',
            labels={'id_aluno': 'Número do aluno', 'nome': 'Aluno'}
        )
        st.plotly_chart(fig)
else:
    with tab2:
        st.write("Nenhum dado disponível para o aluno selecionados.")


