import random

def generate_pedido_sql(num_pedidos=500):
    cliente_ids = list(range(1, 1001))  # Supondo que tenhamos 1000 clientes
    produto_ids = list(range(1, 80))   # Supondo que tenhamos 80 produtos

    pedido_inserts = []
    item_pedido_inserts = []

    # Distribuições de itens
    distribuicoes = [
        (50, 1, 1, 3),   # 10% dos pedidos com 1 item
        (100, 2, 1, 2),  # 20% dos pedidos com 2 itens
        (150, 3, 2, 4),  # 30% dos pedidos com 3 itens
        (25, 1, 1, 3),   # 5% dos pedidos com 1 item
        (100, 2, 1, 2),  # 20% dos pedidos com 2 itens
        (75, 3, 2, 4)    # 25% dos pedidos com 3 itens
    ]

    pedido_count = 1
    for distribuicao in distribuicoes:
        for _ in range(distribuicao[0]):
            cliente_id = random.choice(cliente_ids)
            data_pedido = f"2022-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}"
            pedido_inserts.append(f"({pedido_count}, {cliente_id}, '{data_pedido}')")

            produto_id_aux = list()
            for _ in range(distribuicao[1]):  # Número de itens
                produto_id = get_produto_id(produto_id_aux, produto_ids)
                quantidade = random.randint(distribuicao[2], distribuicao[3])
                item_pedido_inserts.append(f"({pedido_count}, {produto_id}, {quantidade}, (SELECT preco FROM produto WHERE id = {produto_id}))")
                produto_id_aux += [produto_id]

            pedido_count += 1

    return pedido_inserts, item_pedido_inserts


def get_produto_id(produto_id_aux, produto_ids):
    produto_id = random.choice(produto_ids)
    if produto_id in produto_id_aux:
        produto_id = get_produto_id(produto_id_aux, produto_ids);
    return produto_id


def main():
    pedidos, itens_pedidos = generate_pedido_sql()

    print("INSERT INTO pedido (id, cliente_id, data_pedido) VALUES")
    for pedido in pedidos[:-1]:
        print(f"{pedido},")
    print(f"{pedidos[-1]};")

    print("\nINSERT INTO item_pedido (pedido_id, produto_id, quantidade, preco_unitario) VALUES")
    for item in itens_pedidos[:-1]:
        print(f"{item},")
    print(f"{itens_pedidos[-1]};")

if __name__ == "__main__":
    main()
