import random

def generate_cpf():
    return ''.join([str(random.randint(0, 9)) for _ in range(11)])

def generate_phone():
    return '11' + ''.join([str(random.randint(0, 9)) for _ in range(8)])

def generate_cep():
    return ''.join([str(random.randint(0, 9)) for _ in range(8)])

def main():
    names = ["Ana", "Bruno", "Carlos", "Daniela", "Eduardo", "Fernanda", "Gabriel", "Helena", "Igor", "Julia"]
    streets = ["Rua Um", "Rua Dois", "Rua Três", "Rua Quatro", "Rua Cinco",
               "Rua Seis", "Rua Sete", "Rua Oito", "Rua Nove", "Rua Dez"]
    bairros = ["Bairro Um", "Bairro Dois", "Bairro Três", "Bairro Quatro", "Bairro Cinco",
               "Bairro Seis", "Bairro Sete", "Bairro Oito", "Bairro Nove", "Bairro Dez"]
    cidades = ["Cidade Um", "Cidade Dois", "Cidade Três", "Cidade Quatro", "Cidade Cinco",
               "Cidade Seis", "Cidade Sete", "Cidade Oito", "Cidade Nove", "Cidade Dez"]
    estados = ["SP", "RJ", "MG", "ES", "RS", "SC", "PR", "BA", "PE", "CE"]

    print("INSERT INTO cliente (nome, cpf, telefone, email, logradouro, numero, complemento, bairro, cidade, estado, cep) VALUES")
    for i in range(1, 1001):
        name = random.choice(names)
        cpf = generate_cpf()
        phone = generate_phone()
        email = f'{name.lower()}{i}@example.com'
        street = random.choice(streets)
        number = str(random.randint(1, 100))
        complemento = f'Apto {random.randint(1, 20)}'
        bairro = random.choice(bairros)
        cidade = random.choice(cidades)
        estado = random.choice(estados)
        cep = generate_cep()
        print(f"('{name}', '{cpf}', '{phone}', '{email}', '{street}', '{number}', '{complemento}', '{bairro}', '{cidade}', '{estado}', '{cep}'){',' if i < 1000 else ';'}")

if __name__ == "__main__":
    main()
