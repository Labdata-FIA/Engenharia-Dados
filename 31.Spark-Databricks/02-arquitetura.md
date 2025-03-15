# A Arquitetura Databricks

A arquitetura do Databricks é projetada para oferecer uma plataforma unificada de análise de dados, aproveitando o poder do Apache Spark para processamentos em larga escala. Ela combina flexibilidade, escalabilidade e governança robusta para soluções de dados e machine learning.

![architecture.png](imagens%2Farchitecture.png)

## Conta Databricks

### Plano de Controle (Control Plane)

Localizado na conta Databricks, este plano gerencia a orquestração dos recursos e serviços principais:

- **Web Application**: Interface gráfica para os usuários interagirem com a plataforma.
- **Compute Orchestration**: Gerenciamento dos clusters de computação.
- **Unity Catalog**: Governança e gerenciamento de dados.
- **Queries and Code**: Execução de consultas e código.

### Plano de Computação Serverless

Este plano oferece uma infraestrutura serverless para execução de workloads, permitindo que o Databricks gerencie automaticamente a computação necessária sem intervenção do usuário.

## Conta na Nuvem do Cliente

O serviço cloud contratado pelo cliente, como Amazon Web Services (AWS), Microsoft Azure ou Google Cloud Platform.

### Plano de Computação Clássico (Classic Compute Plane)

Este plano, localizado na conta de nuvem do cliente, gerencia os recursos de computação tradicionais:

- **Compute**: Clusters gerenciados pelo usuário, utilizados para processar workloads.

### Workspace Storage Bucket

Um bucket de armazenamento associado à conta de nuvem do usuário, onde são armazenados os dados de trabalho e outros artefatos.

## Seus recursos

**Recursos**: Incluem armazenamento de dados e outros serviços de nuvem que são acessados e manipulados pelas instâncias de computação no Classic Compute Plane e Serverless Compute Plane.

## Usuários e Aplicações

**Usuários e Aplicações:** Interagem com o Control Plane através da interface web ou APIs, facilitando a gestão e o processamento dos dados.

## Navegação
- [Anterior](01-introducao.md)
- [Próximo](03-navegacao-inicial.md)
