from fastapi import FastAPI
from pydantic import BaseModel

from ingestao import salvar_na_bronze

app = FastAPI(
    title="FIAShop API",
    version="0.1.0",
    description="Recebe pedidos da FIAShop e grava na camada bronze do MinIO",
)


# O "formato" do pedido. A FastAPI valida automaticamente:
# se faltar um campo ou vier texto onde era número, ela devolve erro 422.
class Pedido(BaseModel):
    id_pedido: int
    cliente: str
    produto: str
    quantidade: int
    valor_unitario: float


@app.get("/")
def home():
    return {"mensagem": "FIAShop API no ar"}


@app.post("/pedidos", status_code=201)
def receber_pedido(pedido: Pedido):
    # model_dump() transforma o pedido em um dicionário Python comum
    caminho = salvar_na_bronze(pedido.model_dump())
    return {"status": "pedido recebido", "arquivo_na_bronze": caminho}
