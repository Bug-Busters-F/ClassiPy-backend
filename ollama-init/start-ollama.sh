#!/bin/bash
set -e

# Pega o modelo da variável de ambiente
MODEL_NAME="${OLLAMA_MODEL:?Erro: variável OLLAMA_MODEL não definida}"

# Verifica se o modelo já foi baixado
if ! ollama list models | grep -q "$MODEL_NAME"; then
    echo "Modelo $MODEL_NAME não encontrado. Fazendo download..."
    ollama pull "$MODEL_NAME"
else
    echo "Modelo $MODEL_NAME já existe. Pulando download."
fi

echo "Iniciando servidor Ollama..."
exec ollama serve
