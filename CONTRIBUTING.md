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
- [Postgres](https://www.postgresql.org/download/) para armazenamento.  
  > **Observação:** Caso não queira instalar o Ollama e o Postgres manualmente, você pode rodá-los via **Docker**. Também é possível rodar o **backend** no Docker junto com eles, o que simplifica a configuração.  
  > **Importante para usuários Windows:** Se você optar por rodar o Postgres no Docker, o backend também precisará rodar dentro de um container Docker, para evitar problemas de conexão.


## Instalação

### 1. Clonar o Repositório


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

5. Abra o arquivo `.env` e edite as credenciais de conexão com o ollama e o banco de dados.

    ```sh
    OLLAMA_MODEL= # Modelo baixado no ollama
    OLLAMA_API_PORT=11434 # Porta padrão do ollama

    DATABASE_URL=postgresql+psycopg2://root:root123@localhost:5432/classipy_database
    ```

### 2. Executando localmente

1. Abra um terminal.

2. Acesse o terminal do Postgres com usuário padrão
   ```bash
   psql -U postgres
   ```

3. Crie o banco de dados
   ```sql
   CREATE DATABASE classipy_database WITH OWNER = postgres;
   ```

4. Saia do terminal do Postgres
   ```bash
   \q
   ```

5. Acesse a pasta do projeto
   ```bash
   cd Classipy-backend
   ```

6. Crie as tabelas do banco
   ```bash
   psql -U postgres -d classipy_database -f postgres-init/init.sql
   ```

### 3. Executando Backend, Postgres e Ollama via Docker

Você pode rodar o **backend**, o **Postgres** e o **Ollama** usando **Docker Compose**, sem precisar instalar nada manualmente.

1. Certifique-se de ter [Docker](https://www.docker.com/) e [Docker Compose](https://docs.docker.com/compose/install/) instalados.  

2. No diretório do projeto, suba os containers:

   ```bash
   docker compose up -d
   ```

   Isso vai iniciar:
   - Backend (porta 8000)  
   - Postgres (porta 5432)  
   - Ollama (porta 11434)  

3. Baixe o modelo LLM desejado no Ollama:
   ```bash
   docker compose exec ollama ollama pull nomeDoModelo
   ```
   Substitua **nomeDoModelo** pelo modelo que você deseja usar. 

   E também baixe **bge-m3**
   ```bash
   docker compose exec ollama ollama pull bge-m3
   ```

### 4. Instalação utilizando um ambiente virtual `venv`

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
   - Instale o navegador necessário para o Playwright
   ```sh
   playwright install chromium
   ```

3. Execute a aplicação

   ```sh
   uvicorn src.main:app --reload
   ```
   Ou execute o comando

   ```sh
   python run.py
   ```

4. Opcional: testar a conexão com o banco
   ```sh
   python -m src.database.test_db_connection
   ```

5. Opcional: preencher as tabelas com dados fictícios
   ```sh
   python seed_local.py
   ```

### 5. Acesse a Aplicação

- O FastAPI está disponível em: [http://localhost:8000](http://localhost:8000)
- Para testar rotas utilize: [http://localhost:8000/docs](http://localhost:8000/docs)
