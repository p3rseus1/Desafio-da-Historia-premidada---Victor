#!/bin/bash

# =============================================================================================================================
# Script em bash para "automatizar ativar o ambiente virtual, instalar bibliotecas e iniciar o servidor web em ambiente local."
# =============================================================================================================================

DIRETORIO=$(pwd)/venv
RAIZ=$(pwd)

# verifica se existe uma variável de ambiente na raiz do projeto
if [ -f "$RAIZ/.env" ]; 
then
    echo "Seu arquivo de .env já existe!"
else
    echo "Insira seu endereço de proxy: exemplo: http://ip:porta"
    read proxy
    echo "PROXY=$proxy" >> .env
    
    if [ $? -eq 0 ];
    then
        echo "Arquivo .env criado com sucesso!"
    else
        echo "Ocorreu algum erro!"
        exit 1
    fi
fi

# verifica se existe um diretorio de ambiente virtual na sua máquina
if [ -d "$DIRETORIO" ];
then
    echo "$DIRETORIO já criado!"
else
    python3 -m venv venv

    if [ $? -eq 0 ];
    then
            echo "Pasta venv criada com sucesso!"
        else 
            echo "Deu algum erro, parando execução do bash."
            exit 1
    fi

    # ativa o ambiente virtual
    source ./venv/bin/activate

    pip install -r requirements.txt

    if [ $? -eq 0 ];
    then
            echo "Bibliotecas necessárias instaladas com sucesso!"
            deactivate
        else 
            echo "Deu algum erro, parando execução do bash."
            exit 1
    fi
fi

# ativa o ambiente virtual
source ./venv/bin/activate

# executa o servidor web 
uvicorn main:app --reload --port 8001