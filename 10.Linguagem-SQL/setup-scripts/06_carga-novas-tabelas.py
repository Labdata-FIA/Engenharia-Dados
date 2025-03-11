import random
from datetime import datetime, timedelta


def generate_transportadoras(n):
    transportadoras = []
    for i in range(1, n+1):
        nome = f"Transportadora {i}"
        email = f"contato{i}@transportadora.com"
        telefone = f"+55119{random.randint(10000000, 99999999)}"
        transportadoras.append((nome, email, telefone))
    return transportadoras

def insert_transportadoras(transportadoras):
    print("INSERT INTO Transportadora (nome, email, telefone) VALUES")
    for nome, email, telefone in transportadoras[:-1]:
        print(f"('{nome}', '{email}', '{telefone}'),")
    nome, email, telefone = transportadoras[-1]
    print(f"('{nome}', '{email}', '{telefone}');")

def insert_formas_pagamento():
    print("\nINSERT INTO forma_pagamento (tipoFormaPagamento) VALUES ('PIX'), ('CartaoCredito');")

def update_pedidos_formas_pagamento(num_pedidos):
    print("\nUPDATE pedido SET forma_pagamento_id = CASE")
    # Assuming 35% PIX (id = 1), 65% Cartão de Crédito (id = 2)
    pix_ids = random.sample(range(1, num_pedidos+1), int(0.35 * num_pedidos))
    for i in range(1, num_pedidos+1):
        forma_pagamento_id = 1 if i in pix_ids else 2
        print(f"WHEN id = {i} THEN {forma_pagamento_id}")
    print("END;")

def distribute_entregas(num_pedidos, num_transportadoras):
    print("\nINSERT INTO entrega (pedido_id, transportadora_id, data_prevista, data_entrega) VALUES")
    atrasados_ids = random.sample(range(1, num_pedidos+1), int(0.15 * num_pedidos))  # 15% de pedidos atrasados
    for pedido_id in range(1, num_pedidos+1):
        transportadora_id = random.randint(1, num_transportadoras)
        if pedido_id in atrasados_ids:
            # Atrasar entrega por 1 a 5 dias adicionais
            int_data_entrega = random.randint(1, 5)
        else:
            # Entrega no prazo ou até antes
            int_data_entrega = 0 - timedelta(days=random.randint(0, 3))
        print(f"({pedido_id}, {transportadora_id}, (select DATE_ADD(data_pedido, INTERVAL 5 DAY) from pedido where id = {pedido_id}), (select DATE_ADD(DATE_ADD(data_pedido, INTERVAL 5 DAY) from pedido where id = {pedido_id}), INTERVAL {int_data_entrega} DAY) from pedido where id = {pedido_id})),")


def main():
    transportadoras = generate_transportadoras(15)
    insert_transportadoras(transportadoras)
    insert_formas_pagamento()
    update_pedidos_formas_pagamento(500)


if __name__ == "__main__":
    main()
