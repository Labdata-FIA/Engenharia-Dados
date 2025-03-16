FROM jupyter/pyspark-notebook

USER root

WORKDIR /home/src

# # Instalar dependências
RUN curl https://install.duckdb.org | sh

# # Exportar o PATH corretamente para o DuckDB
ENV PATH="/home/jovyan/.duckdb/cli/latest:$PATH"

ADD requirements.txt .
RUN pip install -r requirements.txt



