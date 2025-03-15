FROM apache/airflow:2.7.2-python3.11

# Instalar dependências do sistema
USER root
RUN apt-get update && apt-get install -y \
    openjdk-11-jdk \
    build-essential \
    python3-dev \
    gcc \
    libffi-dev \
    libssl-dev \
    && apt-get clean

# Configurar JAVA_HOME
ENV JAVA_HOME /usr/lib/jvm/java-11-openjdk-amd64/
ENV PATH $JAVA_HOME/bin:$PATH

# Instalar dependências do Python
USER airflow
#COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install --upgrade apache-airflow-providers-openlineage>=1.8.0
#RUN pip install -r requirements.txt

