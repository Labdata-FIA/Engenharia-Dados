# Criação do Workspace Databricks com Terraform

Este tutorial será tem como objetivo criar um Workspace Databricks utilizando a AWS utilizando o terraform. 

## Requisitos
- Ter uma conta na AWS os políticas de AdministratorAccess
- Ter o AWS CLI instalado
- Ter o terraform instalado
- Ter um ambiente terminal Linux ou MacOS

## Sumario
- [Contratar a Databricks utilizando o AWS Marketplace](#contratar-a-databricks-utilizando-o-marketplace)
- [Criação da Service Principal Databricks terraform](#criacao-da-service-principal-databricks-terraform)
- [Criação do usuário terraform na Conta AWS](#criacao-do-usuario-terraform-na-conta-aws)
- [Capturar o AccountID da Conta Databricks](#capturar-o-accountid-da-conta-databricks)
- [Configurar acesso do serviço AWS CLI](#configurar-acesso-da-ferramenta-aws-cli)
- [Executar a criação da infraestrutura utilizando terraform](#executar-a-criacao-da-infraestrutura-utilizando-terraform)
- [Executar a destruição da infraestrutura utilizando terraform](#executar-a-destruicao-da-infraestrutura-utilizando-terraform)

### Contratar a Databricks utilizando o Marketplace

#### Pagina Home do Console da AWS
- Após a realização do login no **Console da AWS**

- ![01-aws-console.png](imagens%2Fconfigurar-databricks-aws%2F01-aws-console.png)

#### Navegar até o AWS Marketplace

- Digitar na barra de pesquisa de serviços `AWS Marketplace`
- Clicar no `AWS Marketplace`
![02-aws-console.png](imagens%2Fconfigurar-databricks-aws%2F02-aws-console.png)

- Será carregada a tela Home do `AWS Marketplace`
 
![03-mkt-descobrir-produtos.png](imagens%2Fconfigurar-databricks-aws%2F03-mkt-descobrir-produtos.png)

- Clicar no menu lateral `Descobrir produtos`

![04-mkt-descobrir-produtos.png](imagens%2Fconfigurar-databricks-aws%2F04-mkt-descobrir-produtos.png)

- Utilizar o `Pesquisar AWS Marketplace produtos` e digitar `Databricks, Inc`
- Clicar em `Databricks Data Intelligence Plataform`

![05-mkt-descobrir-produtos.png](imagens%2Fconfigurar-databricks-aws%2F05-mkt-descobrir-produtos.png)

- Será apresentada a tela abaixo

![06-mkt-databricks.png](imagens%2Fconfigurar-databricks-aws%2F06-mkt-databricks.png)

- Clicar em `View purchase options`

![07-mkt-databricks.png](imagens%2Fconfigurar-databricks-aws%2F07-mkt-databricks.png)

- Será apresentada a tela abaixo
![08-mkt-databricks.png](imagens%2Fconfigurar-databricks-aws%2F08-mkt-databricks.png)

- Clicar em `Subcribe`
![09-mkt-databricks.png](imagens%2Fconfigurar-databricks-aws%2F09-mkt-databricks.png)

- Foi contrato o serviço e será apresentada a tela abaixo
![10-mkt-databricks.png](imagens%2Fconfigurar-databricks-aws%2F10-mkt-databricks.png)

- Clicar em `Set up your account`
![11-mkt-databricks.png](imagens%2Fconfigurar-databricks-aws%2F11-mkt-databricks.png)

- Será apresentada a tela abaixo e informar:
  - E-mail (Conta que será criada na Databricks)
  - First name (Nome)
  - Last name (Sobrenome)
  - Company (Empresa)
![12-databricks.png](imagens%2Fconfigurar-databricks-aws%2F12-databricks.png)

- Ir até a caixa de e-mail informada no passo anterior e identificaro e-mail de boas-vindas da Databricks
  - Clicar em `Log in to get started`
![13-databricks.png](imagens%2Fconfigurar-databricks-aws%2F13-databricks.png)

- Ir até a caixa de e-mail e recuperar o código de vericação para inserir na tela abaixo
![14-databricks.png](imagens%2Fconfigurar-databricks-aws%2F14-databricks.png)

- Será apresentada uma tela te convidando para ser criado o teu primeiro workspace
  - (Não será criado o workspace por este caminho), mas informar os dados apenas para destravar a navegação
  - Informar o nome do workspace `teste`
  - Escolher a region `us-east-1`
  - Clicar no botão `Start Quickstart` 
  - Será aberta outra aba para seguir com a implantação utilizando `CloudFormation`
  - Voltando para a aba anterior, será apresentada a tela abaixo

![15-databricks.png](imagens%2Fconfigurar-databricks-aws%2F15-databricks.png)

- **Parabéns!!!! Foi finalizada a etapa de criação da Conta Databricks vinculada a conta da AWS**

> Clicar no canto superior esquerdo `Account` e Salvar no favoritos a pagina após o carregamento

![16-databricks.png](imagens%2Fconfigurar-databricks-aws%2F16-databricks.png)

[Voltar ao Sumário](#sumario)

### Criacao da Service Principal Databricks `terraform`

Os passos abaixo tem como objetivo criar a service principal que será utilizado pelo serviço *terraform*.

- Tendo como ponto de partida a tela abaixo

![16-databricks.png](imagens%2Fconfigurar-databricks-aws%2F16-databricks.png)

- Clicar no **menu User management**

![17-databricks.png](imagens%2Fconfigurar-databricks-aws%2F17-databricks.png)

- Clicar na aba **Service principals**
  - Clicar no botão `Add service principal`
![18-databricks.png](imagens%2Fconfigurar-databricks-aws%2F18-databricks.png)

- Informar `terraform` no nome da service principal e clicar no botão `Add`

![19-databricks.png](imagens%2Fconfigurar-databricks-aws%2F19-databricks.png)

- Após a criação da service principal terraform, clique novamente no link `terraform` para carregar a tela de edição
![21-databricks.png](imagens%2Fconfigurar-databricks-aws%2F21-databricks.png)

- Será apresentada a tela abaixo

![22-databricks.png](imagens%2Fconfigurar-databricks-aws%2F22-databricks.png)

- Clique no botão `Generate secret`

![23-databricks.png](imagens%2Fconfigurar-databricks-aws%2F23-databricks.png)

- Guardar as credenciais `Secret` e `Client ID`, após guardar os dados da tela abaixo em um arquivo txt por exemplo, clicar no botão `Done`

> Atenção, somente neste passo você terá acesso a `Secret`, senão será necessário criar novamente.

![24-databricks.png](imagens%2Fconfigurar-databricks-aws%2F24-databricks.png)

- Clicar na aba *Roles* e será apresentada a tela baixo

![25-databricks.png](imagens%2Fconfigurar-databricks-aws%2F25-databricks.png)

- Ativar a opção `Account admin` conforme apresentada na tela abaixo

![26-databricks.png](imagens%2Fconfigurar-databricks-aws%2F26-databricks.png)

[Voltar ao Sumário](#sumario)

### Criacao do usuario terraform na Conta AWS

Tendo como ponto de partida a tela Home do Console da AWS

- Digitar na barra de pesquisa de serviços `IAM` (Identity And Access Management)
  - Clicar no Serviço `IAM`
![27-aws.png](imagens%2Fconfigurar-databricks-aws%2F27-aws.png)

- Será apresentada a tela abaixo o Identity And Access Management - IAM
  - Clicar no **menu Usuários**

![28-aws.png](imagens%2Fconfigurar-databricks-aws%2F28-aws.png)

- Será apresentada a tela abaixo e clicar no botão `Criar usuário`

![29-aws.png](imagens%2Fconfigurar-databricks-aws%2F29-aws.png)

- Informar o nome do usuário `terraform` e clicar em `Próximo`

![30-aws.png](imagens%2Fconfigurar-databricks-aws%2F30-aws.png)

- Será apresentada a tela abaixo

![31-aws.png](imagens%2Fconfigurar-databricks-aws%2F31-aws.png)

- Clicar na opção `Anexar políticas diretamente`

![32-aws.png](imagens%2Fconfigurar-databricks-aws%2F32-aws.png)

- Utilizar a caixa de pesquisa abaixo informando `AdministratorAccess`

![33-aws.png](imagens%2Fconfigurar-databricks-aws%2F33-aws.png)

- Como é um tela grande, seguem os passos:
  1. Na caixa de pesquisa abaixo informando `AdministratorAccess`
  2. Selecionar a política `AdministratorAccess`
  3. Clicar no botão `Próximo`

![34-aws.png](imagens%2Fconfigurar-databricks-aws%2F34-aws.png)

- Será apresentada a tela abaixo e clicar no botão `Criar usuário`

![35-aws.png](imagens%2Fconfigurar-databricks-aws%2F35-aws.png)

- Será apresentada a tela abaixo após a criação, clicar no link `terraform` para fazer a edição do usuário

![36-aws.png](imagens%2Fconfigurar-databricks-aws%2F36-aws.png)

- Será necessário criar chave de acesso permitindo que a ferramenta terraform use este usuário
  - Clicar em `Criar chave de acesso`

![37-aws.png](imagens%2Fconfigurar-databricks-aws%2F37-aws.png)

- Selecionar a opção `Command Line Interface (CLI)`

![38-aws.png](imagens%2Fconfigurar-databricks-aws%2F38-aws.png)

- Descer a barra de rolagem
  - Marcar a opção `Compreendo a recomendação acima e quero processeguir para criar uma chave de acesso`
  - Clicar no botão `Próximo`

![39-aws.png](imagens%2Fconfigurar-databricks-aws%2F39-aws.png)

- Informar a descrição da Tag o valor `Terraform fará acesso via terminal aws cli`
- Clicar no botão `Criar chave de acesso`

![40-aws.png](imagens%2Fconfigurar-databricks-aws%2F40-aws.png)

- Será apresentada a tela abaixo
  1. Fazer o download das credências clicando no botão `Baixar arquivo .csv`
  2. Clicar no botão `Concluído`

![41-aws.png](imagens%2Fconfigurar-databricks-aws%2F41-aws.png)

[Voltar ao Sumário](#sumario)

### Capturar o AccountID da Conta Databricks

O AccountID será utilizado para parametrizar o terraform informando qual a conta da Databricks que será manipulada

- Vá até página Home Account Console da Databricks
  1. Clique no canto superior direito na iniciais do usuário
  2. Clique no ícone `copiar`
  3. Guarde O AccountID em txt
![42-databricks.png](imagens%2Fconfigurar-databricks-aws%2F42-databricks.png)

[Voltar ao Sumário](#sumario)

### Configurar o arquivo terraform.tfvars

- O arquivo `terraform.tfvars` tem a responsabilidade de:
  - Conhecer a credênciais de acesso da Conta Databricks
  - Nome do prefixo que será utilizado para criação da infraestrutura
  - Nome da region que será criada a infra-extrutura
  - Nome do projeto dado para criação da infraestrutura

- Local para identificar o arquivo `terraform.tfvars`
  - `terraform/aws-workspace-basic/terraform.tfvars`

- Conteúdo do arquivo
```terraform
prefix                   = "laboratorio-databricks" // ou outro prefixo da tua preferência
databricks_account_id    = "[Informar o AccountID da Conta da Databricks]"
databricks_client_id     = "[Informar o Client ID da Service principal terraform]"
databricks_client_secret = "[Informar o Client Secret da Service principal terraform]"
tags                     = {
  "Project" = "Laboratorio Databricks" // ou outro nome de projeto da tua preferência
}
region = "us-east-1" // ou outra region da tua preferência
```

[Voltar ao Sumário](#sumario)

### Configurar acesso da ferramenta AWS CLI

A documentação de referência da AWS: [Configurar o AWS CLI](https://docs.aws.amazon.com/pt_br/cli/latest/userguide/cli-chap-configure.html)

Serão necessários recuperar as credenciais `aws_access_key_id` e `aws_secret_access_key` criadas no passo [Criacao do usuario terraform na Conta AWS](#criacao-do-usuario-terraform-na-conta-aws)

No nosso caso fizemos a opção da edição do arquivo: `~/.aws/credentials`

Exemplo de arquivo:
```text
[default]
aws_access_key_id = [Colocar aqui aws_access_key_id]
aws_secret_access_key = [Colocar aqui aws_secret_access_key]
```

[Voltar ao Sumário](#sumario)

### Executar a criacao da infraestrutura utilizando terraform

Neste passo faremos a criação da infraestrutura na Conta AWS e na Conta Databricks

#### Requisitos
- Ter o terraform instalado
- Ter o AWS CLI instalado
- Ter o acessso do AWS CLI configurado, item explicado em [Configurar acesso a ferramenta AWS CLI](#configurar-acesso-da-ferramenta-aws-cli)
- Ter o usuário `terraform` configurado na Conta AWS, item explicado em [Criacao do usuario terraform na Conta AWS](#criacao-do-usuario-terraform-na-conta-aws)
- Ter a service principal configurada na Conta Databricks, item explicado em [Criacao da Service Principal Databricks `terraform`](#criacao-da-service-principal-databricks-terraform) 
- Configurar as variáveis do terraform, item explicado em [Configurar o arquivo terraform.tfvars](#configurar-o-arquivo-terraformtfvars) 

#### Passo a passo

- Utilizando o terminal, navegar até a pasta `terraform/aws-workspace-basic`
```shell
cd terraform/aws-workspace-basic
```

- Fazer a inicialização do terraform
```shell
terraform init
```

- Verificar o planejamento da infraestrutura
```shell
terraform plan
```

- Estando tudo ok, fazer a criação da infraestrutura
```shell
terraform apply
```

- Será solicitado a resposta **yes**
```text
Plan: 35 to add, 0 to change, 0 to destroy.

Do you want to perform these actions?
  Terraform will perform the actions described above.
  Only 'yes' will be accepted to approve.

  Enter a value: yes
```

- Ao final será apresenta a mensagem abaixo
```text
Apply complete! Resources: 35 added, 0 changed, 0 destroyed.
```

[Voltar ao Sumário](#sumario)

### Dar acesso ao Workspace Databricks 

Neste passo será dado acesso ao usuário ao Workspace Databricks

- Tendo como base a página Home da Console Databricks
  - Clicar no **menu Workspaces**

![43-databricks.png](imagens%2Fconfigurar-databricks-aws%2F43-databricks.png)

- Será apresentada a tela abaixo
  - Clicar no link `laboratorio-databricks` 

![44-databricks.png](imagens%2Fconfigurar-databricks-aws%2F44-databricks.png)

- Clicar na aba **Permissions**

![45-databricks.png](imagens%2Fconfigurar-databricks-aws%2F45-databricks.png)

- Clicar no botão `Add permissions`

![46-databricks.png](imagens%2Fconfigurar-databricks-aws%2F46-databricks.png)

- Selecionar o usuário desejado

![47-databricks.png](imagens%2Fconfigurar-databricks-aws%2F47-databricks.png)

- Informar o perfil de acesso, no nosso caso será `Admin`

![48-databricks.png](imagens%2Fconfigurar-databricks-aws%2F48-databricks.png)

- Clicar no botão `Save`

![49-databricks.png](imagens%2Fconfigurar-databricks-aws%2F49-databricks.png)

- Como exemplo, será apresentada a tela abaixo

![50-databricks.png](imagens%2Fconfigurar-databricks-aws%2F50-databricks.png)

[Voltar ao Sumário](#sumario)

### Executar a destruicao da infraestrutura utilizando terraform

Neste passo faremos a destruição da infraestrutura na Conta AWS e na Conta Databricks

- Utilizando o terminal, navegar até a pasta `terraform/aws-workspace-basic`
```shell
cd terraform/aws-workspace-basic
```

- Fazer a destruição da infraestrutura
```shell
terraform destroy
```

- Será solicitado a resposta **yes**
```text
Plan: 0 to add, 0 to change, 35 to destroy.

Do you really want to destroy all resources?
  Terraform will destroy all your managed infrastructure, as shown above.
  There is no undo. Only 'yes' will be accepted to confirm.

  Enter a value: yes
```

[Voltar ao Sumário](#sumario)

# Navegação
- [README](README.md)
