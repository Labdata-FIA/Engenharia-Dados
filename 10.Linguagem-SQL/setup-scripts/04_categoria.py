import random

def generate_categories():
    categories = []
    for i in range(1, 31):
        name = f"Categoria {i}"
        description = f"Descrição da Categoria {i}"
        categories.append((name, description))
    return categories

def generate_product_categories(num_products=80, num_categories=30):
    product_categories = set()  # Use set to avoid duplicates
    for _ in range(100):  # Generate more associations to ensure good distribution
        product_id = random.randint(1, num_products)
        category_id = random.randint(1, num_categories)
        product_categories.add((product_id, category_id))
    return list(product_categories)

def main():
    categories = generate_categories()
    product_categories = generate_product_categories()

    print("INSERT INTO Categoria (nome, descricao) VALUES")
    for i, (name, description) in enumerate(categories):
        print(f"('{name}', '{description}'){',' if i < len(categories) - 1 else ';'}")

    print("\nINSERT INTO produto_categoria (produto_id, categoria_id) VALUES")
    for i, (product_id, category_id) in enumerate(product_categories):
        print(f"({product_id}, {category_id}){',' if i < len(product_categories) - 1 else ';'}")

if __name__ == "__main__":
    main()
