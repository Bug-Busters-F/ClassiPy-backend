-- Cria tabela de teste
CREATE TABLE test_table (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insere registros de teste
INSERT INTO test_table (name) VALUES ('Gabriel'), ('Alice'), ('Bob');

-- Consulta para testar
SELECT * FROM test_table;
