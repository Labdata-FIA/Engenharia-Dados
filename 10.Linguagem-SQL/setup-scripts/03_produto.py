import random

def generate_product_inserts():
    products = []
    # Preços variam 10% para os valores de 1 a 10
    for i in range(1, 11):
        price = i * 1.10  # 10% increase
        products.append(f"('Produto {i}', {price:.2f})")

    # Preços variam 20% para os valores de 15 a 20
    for i in range(15, 21):
        price = i * 1.20  # 20% increase
        products.append(f"('Produto {i}', {price:.2f})")

    # Preço fixo de 35 com variação de 15%
    price = 35 * 1.15
    products.append(f"('Produto 21', {price:.2f})")

    # Restante dos produtos com valores variáveis até 100
    for i in range(22, 101):
        price = random.uniform(1, 100)
        products.append(f"('Produto {i}', {price:.2f})")

    return products

def main():
    products = generate_product_inserts()
    print("INSERT INTO produto (nome, preco) VALUES")
    for i, product in enumerate(products):
        print(f"{product}{',' if i < len(products) - 1 else ';'}")

if __name__ == "__main__":
    main()
