import csv

from tabulate import tabulate

CAMINHO_ARQUIVO = 'dados/clientes.csv'


def carregar_clientes(caminho):
    """Lê o CSV e devolve uma lista de dicionários (uma por linha)."""
    registros = []
    with open(caminho, 'r', encoding='utf-8') as f:
        leitor = csv.DictReader(f)  # DictReader: cada linha vira um dicionário
        for linha in leitor:
            registros.append(linha)
    return registros


def mostrar_tabela(registros):
    """Imprime os registros em formato de tabela."""
    print(tabulate(registros, headers='keys', tablefmt='github', disable_numparse=True))


def main():
    registros = carregar_clientes(CAMINHO_ARQUIVO)

    print(f'Total de registros: {len(registros)}')

    if not registros:
        print('O arquivo não tem nenhuma linha de dados.')
        return

    print('Chaves disponíveis:', list(registros[0].keys()))
    print()
    mostrar_tabela(registros)


if __name__ == '__main__':
    main()