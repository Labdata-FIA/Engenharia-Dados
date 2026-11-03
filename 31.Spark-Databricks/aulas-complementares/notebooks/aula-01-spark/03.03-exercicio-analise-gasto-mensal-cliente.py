# Databricks notebook source
# MAGIC %md
# MAGIC ## Exercício: Resultado Acumulado por Mês
# MAGIC
# MAGIC ### Estrutura dos Arquivos
# MAGIC
# MAGIC > path: https://raw.githubusercontent.com/rafael-negrao/laboratorio-spark/main/dados/analise_clientes.csv
# MAGIC
# MAGIC #### Dicionário de Dados
# MAGIC
# MAGIC | Coluna        | Descrição                                             |
# MAGIC |---------------|-------------------------------------------------------|
# MAGIC | `cliente_id`  | Identificador único de cada cliente                   |
# MAGIC | `nome_cliente`| Nome completo do cliente                              |
# MAGIC | `gasto_mensal`| Valor gasto pelo cliente naquele mês (em moeda local) |
# MAGIC | `data_adesao` | Data de adesão do cliente ao serviço                  |
# MAGIC | `plano_id`    | Identificador do plano de assinatura do cliente       |
# MAGIC
# MAGIC #### Preview dos Dados de Clientes
# MAGIC
# MAGIC | cliente_id | nome_cliente     | gasto_mensal | data_adesao | plano_id |
# MAGIC |------------|------------------|--------------|-------------|----------|
# MAGIC | 1          | Paula Silva      | 4671.03      | 2024-08-29  | 1        |
# MAGIC | 2          | Gabriela Pereira | 3177.30      | 2024-12-22  | 1        |
# MAGIC | 3          | Lucas Souza      | 2759.41      | 2024-01-22  | 1        |
# MAGIC | 4          | Maria Almeida    | 2749.62      | 2024-09-13  | 1        |
# MAGIC | 5          | Carlos Oliveira  | 1553.34      | 2024-10-11  | 2        |
# MAGIC
# MAGIC ### Preview do Resultado Acumulado por Mês
# MAGIC
# MAGIC **Objetivo**: Este arquivo é utilizado para analisar o desempenho financeiro mensal e o crescimento acumulado, oferecendo uma visão macro da receita da empresa ao longo do ano.
# MAGIC
# MAGIC | ano  | mes | gasto_mensal | gasto_acumulado |
# MAGIC |------|-----|--------------|-----------------|
# MAGIC | 2024 | 01  | 180,398.82   | 180,398.82      |
# MAGIC | 2024 | 02  | 175,558.67   | 355,957.49      |
# MAGIC | 2024 | 03  | 249,995.38   | 605,952.87      |
# MAGIC | 2024 | 04  | 243,635.11   | 849,587.98      |
# MAGIC | 2024 | 05  | 208,224.93   | 1,057,812.91    |
# MAGIC
# MAGIC #### Dicionário de Dados
# MAGIC
# MAGIC | Coluna          | Descrição                                                            |
# MAGIC |-----------------|----------------------------------------------------------------------|
# MAGIC | `ano`           | Ano da adesão do cliente                                             |
# MAGIC | `mes`           | Mês em que os gastos foram registrados                               |
# MAGIC | `gasto_mensal`  | Soma dos gastos de todos os clientes naquele mês                     |
# MAGIC | `gasto_acumulado`| Valor acumulado do gasto ao longo dos meses, até o mês atual         |
# MAGIC
# MAGIC #### Passos do Exercício
# MAGIC
# MAGIC 1. **Carregar o Arquivos CSV**
# MAGIC 2. **Enriquecer os dados extraindo ano e mês da coluna data_adesao**
# MAGIC 3. **Definir uma especificação de janela para cálculo do gasto acumulado**
# MAGIC 4. **Agrupar os dados por ano e mês, somando os gastos mensais**
# MAGIC 5. **Calcular o gasto acumulado usando a função over para criar o acumulado por ano**
# MAGIC 6. **Formatar os valores de gasto_mensal e gasto_acumulado para duas casas decimais**
# MAGIC 7. **Exibir o Resultado**
# MAGIC
# MAGIC **Bônus**
# MAGIC
# MAGIC - **Salvar os dados na tabela `resultado_acumulado_por_mes`**
# MAGIC

# COMMAND ----------


