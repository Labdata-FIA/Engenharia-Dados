ARG STRIMZI_VERSION=latest-kafka-3.7.0

# -----------------------------------------------------------------------------
# Etapa 1 (temporária): baixa e descompacta o plugin S3 Sink da Confluent.
# O plugin vem em .zip e a imagem do Strimzi não tem o "unzip", por isso usamos
# uma imagem Debian só para essa tarefa (multi-stage build).
# -----------------------------------------------------------------------------
FROM debian:latest AS unzip-layer

RUN apt-get update && apt-get install -y unzip curl

WORKDIR /tmp/connect-plugins

RUN curl -sfSL https://api.hub.confluent.io/api/plugins/confluentinc/kafka-connect-s3/versions/10.5.5/archive -o archive.zip &&\
    unzip archive.zip


# -----------------------------------------------------------------------------
# Etapa 2 (imagem final): Kafka Connect do Strimzi + plugins
# -----------------------------------------------------------------------------
FROM quay.io/strimzi/kafka:${STRIMZI_VERSION} AS imagemfinal

ARG DEBEZIUM_CONNECTOR_VERSION=2.6.1.Final

# Pasta onde o Kafka Connect procura os plugins (plugin.path)
ENV KAFKA_CONNECT_PLUGIN_PATH=/tmp/connect-plugins/
ENV KAFKA_CONNECT_LIBS=/opt/kafka/libs

# Plugins Debezium (Source / CDC): PostgreSQL e SQL Server
# + Debezium Interceptor (usado para tracing na aula de Observabilidade)
RUN mkdir $KAFKA_CONNECT_PLUGIN_PATH &&\
    cd $KAFKA_CONNECT_PLUGIN_PATH &&\
    curl -sfSL  https://repo1.maven.org/maven2/io/debezium/debezium-connector-postgres/${DEBEZIUM_CONNECTOR_VERSION}/debezium-connector-postgres-${DEBEZIUM_CONNECTOR_VERSION}-plugin.tar.gz | tar xz &&\
    cd debezium-connector-postgres &&\
    curl -sfSL  https://repo1.maven.org/maven2/io/debezium/debezium-connector-sqlserver/${DEBEZIUM_CONNECTOR_VERSION}/debezium-connector-sqlserver-${DEBEZIUM_CONNECTOR_VERSION}-plugin.tar.gz | tar xz &&\
    cd debezium-connector-sqlserver &&\
    curl -sfSL https://repo1.maven.org/maven2/io/debezium/debezium-interceptor/${DEBEZIUM_CONNECTOR_VERSION}/debezium-interceptor-${DEBEZIUM_CONNECTOR_VERSION}.jar -o debezium-interceptor-${DEBEZIUM_CONNECTOR_VERSION}.jar

# Copia o plugin S3 Sink (Etapa 1) para a pasta de plugins
COPY --from=unzip-layer /tmp/connect-plugins/confluentinc-kafka-connect-s3-10.5.5 ${KAFKA_CONNECT_PLUGIN_PATH}/confluentinc-kafka-connect-s3-10.5.5
