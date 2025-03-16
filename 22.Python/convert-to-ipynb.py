import nbformat as nbf
import shutil
import json


def convert_md_to_ipynb(input_path, output_path):
    # Reading the content of the uploaded markdown file
    with open(input_path, 'r') as file:
        content = file.read()

    # Split the content by lines
    lines = content.split('\n')

    # Create a new notebook
    nb = nbf.v4.new_notebook()
    cells = []

    # Parse the lines to create appropriate cells
    code_block = False
    code_lines = []

    for line in lines:
        if line.startswith('```python'):
            code_block = True
            if code_lines:
                cells.append(nbf.v4.new_markdown_cell('\n'.join(code_lines)))
                code_lines = []
        elif line.startswith('```') and code_block:
            code_block = False
            cells.append(nbf.v4.new_code_cell('\n'.join(code_lines)))
            code_lines = []
        else:
            code_lines.append(line)

    # Add remaining lines as a markdown cell
    if code_lines:
        if code_block:
            cells.append(nbf.v4.new_code_cell('\n'.join(code_lines)))
        else:
            cells.append(nbf.v4.new_markdown_cell('\n'.join(code_lines)))

    # Assign cells to the notebook
    nb.cells = cells

    # Write the notebook to a file
    with open(output_path, 'w') as file:
        nbf.write(nb, file)


prefix_files = [
    '01,02.introducao',
    '03.variaveis,tipo-de-dados,estruturas',
    '04.estrutura-de-dados',
    '05.operadores',
    '06.estrutura-de-controles',
    '07.estrutura-de-repeticao',
    '08.funcoes',
    '09-tratamento-excecoes',
    '10.01.manipulacao-strings',
    '10.01.manipulacao-strings-garito',
    '10.02.manipulacao-list',
    '10.02.manipulacao-list-gabarito',
    '10.03.manipulacao-set',
    '10.03.manipulacao-set-gabarito',
    '10.04.manipulacao-dict',
    '10.04.manipulacao-dict-gabarito',
    '10.05-trabalhando-com-operadores',
    '10.05-trabalhando-com-operadores-gabarito',
    '10.06-trabalhando-com-funcoes',
    '10.06-trabalhando-com-funcoes-gabarito'
]

prefix_files = filter(lambda s: s in '03.variaveis,tipo-de-dados,estruturas', prefix_files)

# Convert the file
for prefix_file in prefix_files:
    convert_md_to_ipynb(
        f'01.introducao-ao-python/{prefix_file}.md',
        f'01.introducao-ao-python/{prefix_file}.ipynb')
