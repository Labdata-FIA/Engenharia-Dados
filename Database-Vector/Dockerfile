FROM jupyter/pyspark-notebook

# Dependências de sistema para compilar o psycopg2 (exige root)
USER root
RUN apt-get update && apt-get install -y --no-install-recommends \
        libpq-dev gcc \
    && rm -rf /var/lib/apt/lists/*

# Diretório de trabalho, com dono correto para o usuário do notebook
RUN mkdir -p /home/src && chown ${NB_UID}:${NB_GID} /home/src
WORKDIR /home/src

# Volta para o usuário padrão antes de instalar os pacotes Python
USER ${NB_UID}

COPY --chown=${NB_UID}:${NB_GID} requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt