# Databricks notebook source
# MAGIC %md
# MAGIC
# MAGIC ## Exercício: Análise de Vendas
# MAGIC
# MAGIC ### Estrutura dos Arquivos:
# MAGIC
# MAGIC #### Tabela Categoria: `categorias.csv`
# MAGIC
# MAGIC > path: https://raw.githubusercontent.com/rafael-negrao/laboratorio-spark/main/dados/categorias.csv
# MAGIC
# MAGIC | categoria_id | categoria_nome |
# MAGIC |--------------|----------------|
# MAGIC | 1            | Eletrônicos    |
# MAGIC | 2            | Roupas         |
# MAGIC | ...          | ...            |
# MAGIC
# MAGIC #### Tabela de Vendas: `vendas_com_categorias.csv`
# MAGIC
# MAGIC > path: https://raw.githubusercontent.com/rafael-negrao/laboratorio-spark/main/dados/vendas_com_categorias.csv
# MAGIC
# MAGIC | produto_id | categoria_id | produto_nome   | vendas | quantidade |
# MAGIC |------------|--------------|----------------|--------|------------|
# MAGIC | 1          | 2            | Camiseta       | 634.79 | 32         |
# MAGIC | 2          | 5            | Liquidificador | 236.65 | 48         |
# MAGIC | ...        | ...          | ...            | ...    | ...        |
# MAGIC
# MAGIC #### Dicionário de dados:
# MAGIC
# MAGIC 1. **Categoria**:
# MAGIC     - `categoria_id`: Identificador único da categoria.
# MAGIC     - `categoria_nome`: Nome da categoria.
# MAGIC
# MAGIC 2. **Produto**:
# MAGIC     - **`produto_id`**: Identificador único do produto.
# MAGIC     - **`categoria_id`**: Referência à categoria do produto.
# MAGIC     - **`produto_nome`**: Nome do produto, como "Smartphone", "Notebook", "Camiseta", etc.
# MAGIC     - **`vendas`**: Valores aleatórios de venda.
# MAGIC     - **`quantidade`**: Quantidade vendida.
# MAGIC
# MAGIC #### Resultado da análise de vendas
# MAGIC
# MAGIC - Agrupar por categoria de produto e calcular a soma e a média das vendas:
# MAGIC
# MAGIC | categoria_nome    | total_vendas | media_vendas |
# MAGIC |-------------------|--------------|--------------|
# MAGIC | Brinquedos        | 480.15       | 480.15       |
# MAGIC | Eletrodomésticos  | 236.65       | 236.65       |
# MAGIC | Eletrônicos       | 906.37       | 906.37       |
# MAGIC | Livros            | 861.04       | 861.04       |
# MAGIC | Roupas            | 634.79       | 634.79       |
# MAGIC
# MAGIC #### Passos do Exercício
# MAGIC
# MAGIC 1. **Carregar os Arquivos CSV**
# MAGIC 2. **Juntar as Tabelas (Join)**
# MAGIC 3. **Agrupar por Categoria e Calcular as Agregações**
# MAGIC 4. **Exibir o Resultado**
# MAGIC

# COMMAND ----------



# COMMAND ----------



# COMMAND ----------



# COMMAND ----------



# COMMAND ----------


