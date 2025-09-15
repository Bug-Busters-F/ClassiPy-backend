# Como Contribuir - Seu Passaporte de Entrada

Estamos felizes em receber você aqui e saber que está interessado em contribuir para o nosso projeto. Como um projeto de código aberto, cada contribuição é valorizada e ajuda a impulsionar o crescimento e a qualidade do nosso trabalho. Este guia foi criado para orientá-lo sobre como você pode participar e fazer parte da nossa comunidade de desenvolvimento. Estamos ansiosos para ver suas contribuições e trabalhar juntos para tornar nosso projeto ainda melhor!

## Código de Conduta

Para garantir um ambiente respeitável e inclusivo, leia e siga nosso [Código de Conduta](./CODE_OF_CONDUCT.md).

## Começando a Contribuir

Contribuir para o nosso projeto é fácil e estamos ansiosos para receber suas contribuições! Antes de entrarmos nos passos para instalação da aplicação, você precisará configurar algumas ferramentas e preparar seu ambiente de desenvolvimento.

Aqui está o que você precisa:

- Uma conta no [GitHub](https://github.com/)
- O *version control system* [Git](https://git-scm.com/) instalado.
- Um IDE para o desenvolvimento. Recomendamos o [Visual Studio Code](https://code.visualstudio.com).
- A linguagem de programação [Python v3.12](https://www.python.org/downloads/release/python-3120/).
- O runtime [Ollama](https://ollama.com/download) para LLMs locais.

## Instalação

### 1. Baixar um modelo no Ollama
Antes de rodar a aplicação, você precisa baixar um modelo LLM no Ollama. Siga os passos abaixo:

1. Inicie o aplicativo Ollama no seu computador.

2. Baixe o modelo desejado via terminal.

   ```sh
   ollama pull NOME_DO_MODELO
   ```
   Você pode encontrar modelos [aqui](https://ollama.com/library). O projeto esta usando [qwen3:0.6b](https://ollama.com/library/qwen3:0.6b).


### 2. Clonar o Repositório


O primeiro passo é clonar o repositório do projeto para o seu ambiente local.
1. Abra um terminal.

2. Execute o seguinte comando para clonar o repositório:
   ```bash
   git clone https://github.com/Bug-Busters-F/ClassiPy-backend
   ```

3. Navegue até o diretório do projeto:
   ```bash
   cd ClassiPy-backend
   ```

4. Configure as variáveis de ambiente
    ```sh
    cp .env.template .env
    ```

5. Abra o arquivo `.env` e edite as credenciais de conexão com o banco de dados.

    ```sh
    OLLAMA_MODEL= # Modelo baixado no ollama
    OLLAMA_API_PORT=11434 # Porta padrão do ollama
    ```

### 3. Instalação utilizando um ambiente virtual `venv`

1. Crie o ambiente virtual

   ```sh
   python -m venv venv

   # Windows - ative o ambiente
   source venv/Scripts/activate

   # Linux - ative o ambiente
   . venv/bin/activate

   # Mac - ative o ambiente
   source venv/bin/activate
   ```

2. Instale as dependências

   ```sh
   pip install -r requirements.txt
   ```

3. Execute a aplicação

   ```sh
   uvicorn src.main:app --reload
   ```

4. Acesse a Aplicação
- O FastAPI está disponível em: [http://localhost:8000](http://localhost:8000)
- Para testar rotas utilize: [http://localhost:8000/docs](http://localhost:8000/docs)
