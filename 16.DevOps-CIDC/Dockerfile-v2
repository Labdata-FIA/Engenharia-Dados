# Imagem menor e estável
FROM nginx:alpine

# Defina a versão do curl disponível no repositório da imagem base
# Dica: descubra a versão com: docker run --rm nginx:alpine sh -lc 'apk info -v curl'
ARG CURL_VERSION=8.14.1-r1

# Instalação + página em um único RUN (evita DL3059) e pin de versão (resolve DL3018)
RUN --mount=type=cache,target=/var/cache/apk \
    apk add --no-cache curl=${CURL_VERSION} && \
    printf '<h1>Oi Alunos da FIA!</h1>\n' > /usr/share/nginx/html/index.html

# Healthcheck interno do container
HEALTHCHECK --interval=30s --timeout=3s --retries=3 CMD curl -fsS http://localhost/ || exit 1

EXPOSE 80