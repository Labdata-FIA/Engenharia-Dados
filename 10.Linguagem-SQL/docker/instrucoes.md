
# Configuração do Docker Compose e Instruções de Gerenciamento

## Visão Geral

O arquivo `docker-compose.yml` configura dois serviços em um ambiente Docker Compose: `database-dev-mysql` e `cloudbeaver`.

### Serviços

- **database-dev-mysql**: Executa uma instância do MySQL versão 8.0.31. Configurado para expor a porta 3306 (padrão do MySQL) para o host para conexões locais com o banco de dados. Variáveis de ambiente definem o nome do banco de dados, usuário, senha e outras configurações relevantes. Volumes são usados para persistir dados do MySQL no disco local.
- **cloudbeaver**: Executa o CloudBeaver, uma ferramenta de gerenciamento de banco de dados baseada na web, versão 24.0.3. A porta 8978 é mapeada para o host, permitindo acesso via navegador em `http://localhost:8978`. Um volume é configurado para persistir dados da área de trabalho do CloudBeaver.

### Volumes

- Usados para persistir dados entre reinicializações dos contêineres. `./data` para o MySQL e `./cloudbeaver_workspace` para o CloudBeaver.

### Redes

- **database-dev-tier**: Uma rede interna tipo bridge é criada para facilitar a comunicação segura entre o MySQL e o CloudBeaver sem exposição desnecessária a outras redes.

## Comandos para Gerenciamento dos Serviços

### Iniciando Serviços

- **Iniciar todos os serviços**:
  ```bash
  docker-compose up -d
  ```
  O `-d` significa "desanexado" e executa os contêineres em segundo plano.

### Parando Serviços

- **Parar todos os serviços**:
  ```bash
  docker-compose stop
  ```
  Este comando para os contêineres em execução, mas não os remove.

### Parando e Removendo Serviços, Redes e Volumes

- **Parar e remover tudo**:
  ```bash
  docker-compose down
  ```
  Para remover também os volumes nomeados (e assim destruir os dados persistentes), adicione o parâmetro `-v`:
  ```bash
  docker-compose down -v
  ```

## Considerações Finais

- **Persistência de Dados**: Tenha em mente que a remoção de volumes com `docker-compose down -v` resultará na perda de quaisquer dados salvos nos contêineres. Use isso com cautela.
- **Acessando os Serviços**: Após iniciar os serviços, o MySQL estará acessível em `localhost:3306`, e o CloudBeaver poderá ser acessado em `http://localhost:8978` através de qualquer navegador web.
- **Segurança**: As senhas e outras informações sensíveis estão expostas no arquivo `docker-compose.yml`, o que é aceitável para desenvolvimento, mas deve ser tratado com mais cautela em ambientes de produção.


## Navegação
- [README](../README.md)
