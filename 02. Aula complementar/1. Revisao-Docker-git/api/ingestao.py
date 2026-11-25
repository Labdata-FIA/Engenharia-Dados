import json
import os
from datetime import datetime

import boto3

# Configurações vindas das variáveis de ambiente.
# Caminho: .env (raiz) -> docker-compose.yml (environment:) -> container -> aqui.

# Endereço e bucket não são segredo: podem ter um valor padrão.
MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT", "http://minio:9000")
BUCKET_BRONZE = os.getenv("BUCKET_BRONZE", "bronze")

# Credenciais SÃO segredo: nada de valor padrão no código.
# os.environ["..."] dá erro (KeyError) se a variável não existir,
# o que deixa claro na hora que o .env está faltando.
MINIO_USER = os.environ["MINIO_ROOT_USER"]
MINIO_PASSWORD = os.environ["MINIO_ROOT_PASSWORD"]

# Cliente S3 apontando para o MinIO (o MinIO "fala" a mesma língua do Amazon S3)
s3 = boto3.client(
    "s3",
    endpoint_url=MINIO_ENDPOINT,
    aws_access_key_id=MINIO_USER,
    aws_secret_access_key=MINIO_PASSWORD,
    region_name="us-east-1",
)


def garantir_bucket():
    """Cria o bucket da bronze se ele ainda não existir."""
    nomes = [bucket["Name"] for bucket in s3.list_buckets()["Buckets"]]
    if BUCKET_BRONZE not in nomes:
        s3.create_bucket(Bucket=BUCKET_BRONZE)
        print(f"[BRONZE] bucket criado: {BUCKET_BRONZE}")


def salvar_na_bronze(pedido):
    """Recebe um pedido (dicionário) e grava como JSON na camada bronze."""
    garantir_bucket()
    agora = datetime.now()

    # Na bronze o dado entra como chegou, só acrescentamos quando ele chegou
    pedido["recebido_em"] = agora.strftime("%Y-%m-%dT%H:%M:%S")

    # Uma pasta por dia (mesmo padrão coluna=valor da Aula 7)
    caminho = (
        f"pedidos/data_ingestao={agora:%Y-%m-%d}/"
        f"pedido_{pedido['id_pedido']}_{agora:%H%M%S}.json"
    )

    conteudo = json.dumps(pedido, ensure_ascii=False, indent=2)

    s3.put_object(
        Bucket=BUCKET_BRONZE,
        Key=caminho,
        Body=conteudo.encode("utf-8"),
        ContentType="application/json",
    )

    print(f"[BRONZE] gravado: {BUCKET_BRONZE}/{caminho}")
    return f"{BUCKET_BRONZE}/{caminho}"


# Permite testar o script sozinho, sem a API:
#   docker compose exec fiashop-api python ingestao.py
if __name__ == "__main__":
    pedido_teste = {
        "id_pedido": 999,
        "cliente": "Teste Manual",
        "produto": "Caneca FIA",
        "quantidade": 1,
        "valor_unitario": 39.9,
    }
    salvar_na_bronze(pedido_teste)