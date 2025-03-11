# Instruções básicas - CloudBeaver

## Segue o passo a passo para criar uma conexão com o banco de dados MySQL

### 1. Abrir o navegador utilizando o endereço `http://localhost:8978`
![01-setup.png](..%2Fimagens%2Fcloudbeaver%2F01-setup.png)

### 2. Parametrizar o usuário administrador do CloudBeaver
![02-setup.png](..%2Fimagens%2Fcloudbeaver%2F02-setup.png)

### 3. Finalizar a pametrização administrativa do CloudBeaver
![03-setup.png](..%2Fimagens%2Fcloudbeaver%2F03-setup.png)

### 4. Carregar a tela de login
![04-login.png](..%2Fimagens%2Fcloudbeaver%2F04-login.png)

### 5. Fazer login utilizando o usuário **cbadmin** e a senha definida no **passo 2**
![05-login.png](..%2Fimagens%2Fcloudbeaver%2F05-login.png)

### 6. Após o login será apresentada a tela abaixo
![06-connection-templates.png](..%2Fimagens%2Fcloudbeaver%2F06-connection-templates.png)

### 7. Após o login clicar no logo do CloudBeaver
![07-connection-templates.png](..%2Fimagens%2Fcloudbeaver%2F07-connection-templates.png)

### 8. Clicar no menu **+**
![08-desktop.png](..%2Fimagens%2Fcloudbeaver%2F08-desktop.png)

### 9. Clicar em **New Connection**
![09-new-connection.png](..%2Fimagens%2Fcloudbeaver%2F09-new-connection.png)

### 10. Selecionar o tipo de banco de dados **MySQL**
![10-new-connection.png](..%2Fimagens%2Fcloudbeaver%2F10-new-connection.png)

### 11. Preencher com o seguintes dados:
  - Host: **database-dev-mysql**
  - Database: **database-dev-mysql**
  - User name: **root**
  - User password: **root**
  - Marque a opção "**Save credentials**"
![11-new-connection.png](..%2Fimagens%2Fcloudbeaver%2F11-new-connection.png)

### 12. Clique na aba: DRIVER PROPERTIES
  - Marque como **TRUE** a propriedade **allowPublicKeyRetrieval**
![12-new-connection.png](..%2Fimagens%2Fcloudbeaver%2F12-new-connection.png)

### 13. Clique na aba: DRIVER PROPERTIES
  - Marque como **FALSE** a propriedade **useSSL**
![13-new-connection.png](..%2Fimagens%2Fcloudbeaver%2F13-new-connection.png)

### 14. Clique no botão **TEST**
  - Será apresentada a tela **Connection is established**
![14-new-connection.png](..%2Fimagens%2Fcloudbeaver%2F14-new-connection.png)

### 15. Clicar no botão **CREATE**
![15-new-connection.png](..%2Fimagens%2Fcloudbeaver%2F15-new-connection.png)

### 16. Será apresentada a conexao **MySQL@database-dev-mysql** no canto superior esquerdo
![16-desktop.png](..%2Fimagens%2Fcloudbeaver%2F16-desktop.png)

### 17. Parabéns, a tua conexão foi com sucesso!!!
