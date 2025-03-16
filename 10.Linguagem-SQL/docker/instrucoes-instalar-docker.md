# Instalação do Docker

Este documento fornece instruções sobre como instalar o Docker em diferentes sistemas operacionais, incluindo Windows, macOS e Linux Ubuntu.

## Requisitos
- Verifique se o seu sistema atende aos requisitos mínimos para a instalação do Docker. Em particular, para Windows e macOS, o Docker Desktop é recomendado e requer configurações de hardware específicas.

## Windows (Docker Desktop)

### Passo a Passo

1. **Download**:
    - Visite a [página oficial de download do Docker](https://www.docker.com/products/docker-desktop) e baixe a versão mais recente do Docker Desktop para Windows.

2. **Instalação**:
    - Execute o instalador baixado e siga as instruções na tela. Certifique-se de incluir a instalação do WSL 2 quando solicitado, pois é necessário para o Docker Desktop no Windows.

3. **Configuração**:
    - Após a instalação, execute o Docker Desktop.
    - Siga as instruções na tela para completar a configuração inicial.

4. **Verificar a Instalação**:
    - Abra o PowerShell ou Prompt de Comando e digite `docker --version`.
    - Se a versão do Docker for exibida, a instalação foi bem-sucedida.

## macOS (Docker Desktop)

### Passo a Passo

1. **Download**:
    - Visite a [página oficial de download do Docker](https://www.docker.com/products/docker-desktop) e baixe a versão mais recente do Docker Desktop para macOS.

2. **Instalação**:
    - Abra o arquivo `.dmg` baixado e arraste o Docker para a pasta de Aplicações.

3. **Configuração**:
    - Abra o Docker a partir da pasta de Aplicações.
    - Siga as instruções na tela para permitir o Docker e completar a configuração inicial.

4. **Verificar a Instalação**:
    - Abra o Terminal e digite `docker --version`.
    - Se a versão do Docker for exibida, a instalação foi bem-sucedida.

## Linux Ubuntu

### Passo a Passo

1. **Configuração do Repositório**:
    - Abra um terminal.
    - Atualize o índice de pacotes com `sudo apt update`.
    - Instale os pacotes necessários para permitir o `apt` a usar um repositório sobre HTTPS:
      ```
      sudo apt install apt-transport-https ca-certificates curl software-properties-common
      ```

2. **Adicionar o Repositório do Docker**:
    - Adicione a chave GPG oficial do Docker:
      ```
      curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
      ```
    - Adicione o repositório do Docker às fontes do APT:
      ```
      sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
      ```

3. **Instalação do Docker**:
    - Atualize o índice de pacotes com `sudo apt update`.
    - Instale o pacote Docker CE:
      ```
      sudo apt install docker-ce
      ```

4. **Verificar a Instalação**:
    - Verifique se o Docker foi instalado corretamente com o comando:
      ```
      sudo docker --version
      ```
    - Se a versão do Docker for exibida, a instalação foi bem-sucedida.

---
## Navegação
- [README](../README.md)
