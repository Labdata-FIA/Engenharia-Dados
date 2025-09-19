# Modern Data Stack

## Visão Geral do Projeto  
Este projeto faz parte do curso de Engenharia de Dados da **FIA Labdata**, com o propósito de fornecer uma experiência prática com Modern Data Stack. Os alunos aprenderão a ingerir, transformar, modelar e visualizar dados usando uma variedade de ferramentas e plataformas.

### Objetivos  
- Ingerir dados de arquivos **CSV** para um banco de dados **PostgreSQL**.  
- Transferir dados do **PostgreSQL** para o **Snowflake** usando o **Airbyte**.  
- Modelar dados no **Snowflake** utilizando uma arquitetura de três camadas (**staging**, **dimensão/fato**, **marts**).  
- Criar visualizações usando **Power BI**.

## Dados  
Vamos utilizar o dataset **AdventureWorks** para este projeto. O dataset inclui diversos dados de uma empresa de varejo fictícia, como dados de clientes, vendas e produtos.

### Arquivos  
O conjunto de dados é composto pelos seguintes arquivos:  
- `AdventureWorks Calendar Lookup.csv`  
- `AdventureWorks Customer Lookup.csv`  
- `AdventureWorks Product Categories Lookup.csv`  
- `AdventureWorks Product Lookup.csv`  
- `AdventureWorks Product Subcategories Lookup.csv`  
- `AdventureWorks Returns Data.csv`  
- `AdventureWorks Sales Data 2020.csv`  
- `AdventureWorks Territory Lookup.csv`

## Configuração do Ambiente  
### Requisitos  
- **PostgreSQL**  
- **Snowflake**  
- **Airbyte**  
- **Power BI Desktop**  

### Instalação  
Passos detalhados para instalar e configurar o software e ferramentas necessários serão fornecidos em documentos separados ou durante as aulas.

## Schema do Banco de Dados  
Scripts **SQL** para criação de tabelas e ingestão de dados no **PostgreSQL** serão fornecidos. Os alunos deverão criar schemas semelhantes no **Snowflake** como parte do exercício de modelagem de dados.

## Transformação e Carga de Dados  
Usaremos o **Airbyte** para transferir dados do **PostgreSQL** para o **Snowflake**, seguido pela transformação dos dados de acordo com a abordagem de arquitetura de três camadas, através do dbt.

## Visualização de Dados  
Os alunos utilizarão **Power BI** para criar dashboards ou relatórios visuais que forneçam insights sobre os dados. Requisitos específicos para as visualizações serão fornecidos nas diretrizes do projeto.

## Uso do dbt para Processamento de Dados

Este projeto utiliza o **dbt (Data Build Tool)** para realizar a modelagem e transformação dos dados de forma padronizada.

### Comandos principais do dbt

- `dbt debug`  
  Verifica se a configuração do projeto e a conexão com o banco estão corretas.  

- `dbt deps`  
  Baixa as dependências do projeto (se houver pacotes externos).  

- `dbt run`  
  Executa os modelos definidos no projeto e cria/atualiza as tabelas e views no banco de dados.  

- `dbt test`  
  Executa os testes definidos no projeto (ex: verificar valores nulos, unicidade de chaves).  

- `dbt docs generate`  
  Gera a documentação do projeto em formato estático (HTML).  

- `dbt docs serve`  
  Sobe um servidor local para visualizar a documentação.  

### Passo a passo para rodar o projeto

1. Clonar este repositório:
   ```bash
   git clone https://github.com/Labdata-FIA/Engenharia-Dados.git
   cd Engenharia-Dados/37.Processamento-Dados-DBT
   ```

2. Instalar dependências:
   ```bash
   pip install dbt-core dbt-snowflake
   ```
   *(ou substituir `dbt-snowflake` pelo adaptador do seu banco, como `dbt-postgres`, `dbt-bigquery` etc.)*

3. Verificar a conexão:
   ```bash
   dbt debug
   ```

4. Executar os modelos:
   ```bash
   dbt run
   ```

5. Rodar os testes:
   ```bash
   dbt test
   ```

6. (Opcional) Gerar documentação:
   ```bash
   dbt docs generate
   dbt docs serve
   ```

## Contribuição  
Os alunos são incentivados a contribuir com o projeto sugerindo melhorias ou identificando erros. As contribuições devem ser enviadas como *pull requests* para o repositório.

## Informações de Contato  
Para mais informações ou dúvidas sobre o projeto, entre em contato com **Felipe Yoshimoto** em [LinkedIn](https://www.linkedin.com/in/felipe-yoshimoto/).
