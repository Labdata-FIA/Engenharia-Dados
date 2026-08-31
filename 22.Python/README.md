# Aula Python

Este repositório reúne o material do curso de Python aplicado a engenharia de dados.


## História do Python

Python é uma linguagem de programação de alto nível, interpretada e de propósito geral, conhecida por sua simplicidade e legibilidade. Ela foi criada por Guido van Rossum e foi lançada pela primeira vez em 1991.

### Linha do tempo

* **Final dos anos 1980** — Guido van Rossum começou a trabalhar no Python no Centro de Pesquisa para Matemática e Informática (CWI) em Amsterdã, Holanda. Ele queria desenvolver uma linguagem de programação que pudesse ser usada por programadores iniciantes e experientes, que fosse simples de ler e escrever, e que tivesse uma sintaxe clara.
* **1989** — Guido van Rossum começou o desenvolvimento do Python como um projeto de hobby durante as férias de Natal. Ele se inspirou em várias linguagens, como ABC, C, C++, Algol-68, Modula-3 e Smalltalk.
* **1991** — A primeira versão do Python (versão 0.9.0) foi lançada publicamente. Esta versão já incluía muitas das principais funcionalidades do Python moderno, como exceções, funções e os tipos de dados centrais (`str`, `list`, `dict`).
* **1994** — Foi lançada a versão 1.0 do Python. Esta versão introduziu recursos como o sistema de módulos, que permitia a reutilização de código entre programas.
* **2000** — A Python Software Foundation (PSF) foi criada para gerenciar o desenvolvimento do Python e proteger a linguagem. Neste ano, foi lançada a versão 2.0, que trouxe várias melhorias, como o garbage collection e a compreensão de listas.
* **2008** — Foi lançada a versão 3.0 do Python (também conhecida como Python 3000 ou Py3k). Esta versão não era compatível retroativamente com a série 2.x, introduzindo muitas mudanças significativas para corrigir falhas de design da linguagem e melhorar sua consistência. Algumas das mudanças incluem a mudança na sintaxe do `print` de uma declaração para uma função e a alteração na maneira como a divisão de inteiros funciona.
* **Atualmente** — Python continua a evoluir, com novas versões sendo lançadas regularmente, adicionando novos recursos, melhorias de desempenho e correções de bugs. A comunidade Python é ativa e vibrante, contribuindo com uma vasta gama de bibliotecas e frameworks que tornam Python uma escolha popular para muitas áreas da computação, incluindo desenvolvimento web, ciência de dados, automação, e muito mais.

## Características do Python

Python é uma linguagem de programação poderosa e versátil, que oferece uma série de características que a tornam única e popular entre programadores de todos os níveis de experiência.

## Ambiente

Suba o ambiente com Docker Compose:

```sh
docker compose up -d python-lab
```

Acesse o Jupyter em **http://localhost:8890** — não há senha nem token.

Para parar o ambiente:

```sh
docker compose down python-lab
```

## Python para Engenheiros de Dados


* [Aula 1 — Contexto e tipos de dados](Python-Para-Engenheiros-Dados%2Faula_01_contexto.ipynb)
* [Aula 2 — Coleções de dados](Python-Para-Engenheiros-Dados%2Faula_02_colecoes.ipynb)
* [Aula 3 — Lógica e condições](Python-Para-Engenheiros-Dados%2Faula_03_logica_.ipynb)
* [Aula 4 — Funções](Python-Para-Engenheiros-Dados%2Faula_04_funcoes.ipynb)
* [Aula 5 — Arquivos e formatos](Python-Para-Engenheiros-Dados%2Faula_05_arquivos.ipynb)
* [Aula 6 — Mini-pipeline ETL](Python-Para-Engenheiros-Dados%2Faula_06_pipeline.ipynb)


## Ambiente

O curso roda no **Google Colab** — não é preciso instalar nada. Abra o notebook da aula e execute as células com `Shift + Enter`.

Para rodar localmente (opcional):

* [Instalação do Poetry no Windows](00.instrucoes-ambiente%2Ftutorial-instalacao-poetry-windows.md)
* [Instalação do Poetry no Linux](00.instrucoes-ambiente%2Ftutorial-instalacao-poetry-linux.md)