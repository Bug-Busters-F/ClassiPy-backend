-- Inserir dados na tabela tipi
INSERT INTO tipi (descricao, aliquota, ncm) VALUES
('Reatores nucleares; elementos combustíveis (cartuchos) não irradiados, para reatores nucleares; máquinas e aparelhos para a separação de isótopos.', 0.00, '84011000'),
('Caldeiras de vapor (geradores de vapor), excluindo as caldeiras para aquecimento central...', 0.00, '84021100'),
('Motores de pistão, alternativo ou rotativo, de ignição por centelha (faísca) (motores de explosão).', 3.25, '84071000');

-- Inserir dados na tabela fabricante
INSERT INTO fabricante (fab_nome, fab_endereco, fab_pais) VALUES
('Fornecedor A', '123 Ling Ling Street, Shanghai, China', 'China'),
('Fornecedor B', '456 Innovation Drive, Silicon Valley, USA', 'Estados Unidos'),
('Fornecedor C', '789 Autobahn Avenue, Berlin, Germany', 'Alemanha');

-- Inserir dados na tabela produto
-- Assumindo que os IDs de tipi e endereco são 1, 2, 3...
INSERT INTO produto (part_number, descricao, fornecedor, status_produto, id_tipi, id_endereco) VALUES
('PN-TESTE-01', 'Produto de Teste 1', 'Fornecedor Teste A', true, 1, 1),
('PN-TESTE-02', 'Produto de Teste 2', 'Fornecedor Teste B', false, 3, 3),
('PN-TESTE-03', 'Produto de Teste 3', 'Fornecedor Teste C', true, 2, 2);

-- Inserir dados na tabela historico
-- Assumindo que os IDs de produto são 1, 2, 3...
INSERT INTO historico (hash_code, produto_id) VALUES
('hash_ficticio_para_produto_1_rev1', 1),
('hash_ficticio_para_produto_1_rev2', 1),
('hash_ficticio_para_produto_2', 2),
('hash_ficticio_para_produto_3', 3);