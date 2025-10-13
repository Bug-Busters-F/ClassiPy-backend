-- Inserir dados na tabela tipi
INSERT INTO tipi (descricao, aliquota, ncm) VALUES
('Reatores nucleares; elementos combustíveis (cartuchos) não irradiados, para reatores nucleares; máquinas e aparelhos para a separação de isótopos.', 0.00, '84011000'),
('Caldeiras de vapor (geradores de vapor), excluindo as caldeiras para aquecimento central...', 0.00, '84021100'),
('Motores de pistão, alternativo ou rotativo, de ignição por centelha (faísca) (motores de explosão).', 3.25, '84071000');

-- Inserir dados na tabela endereco
INSERT INTO endereco (pais_origem, endereco_completo) VALUES
('China', '123 Ling Ling Street, Shanghai, China'),
('Estados Unidos', '456 Innovation Drive, Silicon Valley, USA'),
('Alemanha', '789 Autobahn Avenue, Berlin, Germany');

-- Inserir dados na tabela produto
-- Assumindo que os IDs de tipi e endereco são 1, 2, 3...
INSERT INTO produto (part_number, descricao, fornecedor, status_produto, id_tipi, id_endereco) VALUES
('PN-12345-A', 'Componente Eletrônico Principal', 'Fornecedor A', true, 1, 1),
('PN-67890-B', 'Motor de Alta Performance', 'Fornecedor B', false, 3, 3),
('PN-ABCDE-C', 'Peça Mecânica de Precisão', 'Fornecedor C', true, 2, 2);

-- Inserir dados na tabela historico
-- Assumindo que os IDs de produto são 1, 2, 3...
INSERT INTO historico (hash_code, produto_id) VALUES
('hash_para_produto_1_rev1', 1),
('hash_para_produto_1_rev2', 1),
('hash_para_produto_2', 2),
('hash_para_produto_3', 3);