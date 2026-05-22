USE DATABASE ecommerce_lab;

-- 1. CATEGORIAS
INSERT INTO categorias (categoria_id, nome_categoria, descricao) VALUES 
(1, 'Bebidas', 'Sucos, cafés, chás, refrigerantes e cervejas artesanais'),
(2, 'Condimentos', 'Molhos, temperos, conservas e especiarias'),
(3, 'Doces', 'Sobremesas, doces finos e pães doces'),
(4, 'Laticínios', 'Queijos, iogurtes, manteigas e leites especiais'),
(5, 'Grãos/Cereais', 'Pães rústicos, massas frescas e cereais matinais'),
(6, 'Carnes/Aves', 'Cortes selecionados, embutidos e defumados'),
(7, 'Hortifruti', 'Frutas orgânicas, legumes e vegetais frescos'),
(8, 'Frutos do Mar', 'Peixes de água doce, salgada e crustáceos');

-- 2. CLIENTES
INSERT INTO clientes (cliente_id, nome_empresa, nome_contato, titulo_contato, endereco, cidade, regiao, codigo_postal, pais, telefone) VALUES 
('MERC01', 'Mercado Central Ltda', 'João Pereira', 'Gerente de Compras', 'Rua das Flores, 150', 'São Paulo', 'SP', '01001-000', 'Brasil', '(11) 3322-1100'),
('REST02', 'Restaurante Sabor & Arte', 'Maria Silva', 'Proprietária', 'Av. Paulista, 900', 'São Paulo', 'SP', '01310-100', 'Brasil', '(11) 98877-6655'),
('HOTE03', 'Hotel Mar Azul', 'Carlos Souza', 'Coordenador de Eventos', 'Av. Oceânica, 500', 'Salvador', 'BA', '40010-000', 'Brasil', '(71) 3030-4040');

-- 3. FUNCIONARIOS
INSERT INTO funcionarios (funcionario_id, sobrenome, nome, titulo, titulo_cortesia, data_nascimento, data_contratacao, endereco, cidade, regiao, codigo_postal, pais, telefone_residencial, extensao, notas, reporta_a, caminho_foto, salario) VALUES 
(1, 'Oliveira', 'Ricardo', 'Gerente de Vendas', 'Sr.', '1985-05-20', '2020-02-10', 'Rua Chile, 45', 'Curitiba', 'PR', '80001-000', 'Brasil', '(41) 3222-1111', '101', 'Experiência em mercados internacionais.', NULL, '/fotos/emp01.jpg', 8500.00),
(2, 'Santos', 'Beatriz', 'Representante Comercial', 'Sra.', '1992-08-15', '2022-01-05', 'Rua das Palmeiras, 12', 'Porto Alegre', 'RS', '90001-000', 'Brasil', '(51) 3444-2222', '102', 'Especialista em vinhos e bebidas.', 1, '/fotos/emp02.jpg', 4200.00);

-- 4. TRANSPORTADORAS
INSERT INTO transportadoras (transportadora_id, nome_empresa, telefone) VALUES 
(1, 'Logística Rápida S.A.', '(11) 4002-8922'),
(2, 'Entrega Unificada', '(21) 3344-5566'),
(3, 'Expresso Federal', '(41) 98877-6655');

-- 5. FORNECEDORES
INSERT INTO fornecedores (fornecedor_id, nome_empresa, nome_contato, titulo_contato, endereco, cidade, regiao, codigo_postal, pais, telefone, fax, pagina_inicial) VALUES 
(1, 'Líquidos Exóticos', 'Ana Paula Souza', 'Gerente de Compras', 'Rua das Flores, 123', 'São Paulo', 'SP', '01001-000', 'Brasil', '(11) 5555-1234', '', 'www.liquidos.com.br'),
(2, 'Delícias do Sertão', 'Marcos Oliveira', 'Administrador', 'Av. Central, 45', 'Fortaleza', 'CE', '60001-000', 'Brasil', '(85) 3222-4444', '', 'www.sertao.com.br'),
(6, 'Sabor de Minas', 'Mariana Neves', 'Vendas', 'Rua da Bahia, 50', 'Belo Horizonte', 'MG', '30100-000', 'Brasil', '(31) 3444-1010', '', 'www.saborminas.com.br'),
(7, 'Oceania Ltda', 'João Silva', 'Gerente de Vendas', 'Avenida Oceânica, 100', 'Salvador', 'BA', '40000-000', 'Brasil', '(71) 3030-2020', '', ''),
(10, 'Refrescos Americanos LTDA', 'Carlos Dias', 'Diretor Comercial', 'Av. das Nações, 12.890', 'Porto Alegre', 'RS', '90000-000', 'Brasil', '(51) 3555-4640', '', '');

-- 6. PRODUTOS
INSERT INTO produtos (produto_id, nome_produto, fornecedor_id, categoria_id, quantidade_por_unidade, preco_unitario, unidades_em_estoque, unidades_encomendadas, nivel_reordenacao, descontinuado) VALUES 
(1, 'Suco de Cupuaçu 500ml', 1, 1, '12 garrafas', 15.50, 40, 0, 10, FALSE),
(2, 'Café Arábica Especial', 1, 1, 'Pacote 500g', 32.00, 100, 20, 15, FALSE),
(3, 'Molho de Pimenta Malagueta', 2, 2, 'Frasco 100ml', 12.90, 55, 0, 5, FALSE),
(4, 'Tempero Caseiro Nordestino', 2, 2, 'Pote 200g', 8.50, 80, 10, 20, FALSE),
(5, 'Queijo Canastra Real', 6, 4, 'Peça 1kg', 85.00, 25, 5, 5, FALSE),
(6, 'Doce de Leite Viçosa', 6, 3, 'Lata 400g', 22.00, 60, 0, 10, FALSE),
(7, 'Camarão Rosa Congelado', 7, 8, 'Pacote 1kg', 110.00, 15, 10, 5, FALSE),
(9, 'Guaraná Natural 2L', 10, 1, '6 unidades', 48.00, 200, 50, 40, FALSE);

-- 7. PEDIDOS (Observar o CLUSTER BY data_pedido no Snowflake)
INSERT INTO pedidos (pedido_id, cliente_id, funcionario_id, data_pedido, data_requerida, data_envio, enviar_via, frete, nome_envio, endereco_envio, cidade_envio, regiao_envio, codigo_postal_envio, pais_envio) VALUES 
(101, 'MERC01', 2, '2026-04-10', '2026-04-15', '2026-04-12', 1, 45.00, 'Mercado Central Ltda', 'Rua das Flores, 150', 'São Paulo', 'SP', '01001-000', 'Brasil'),
(102, 'REST02', 2, '2026-04-12', '2026-04-18', '2026-04-13', 2, 25.50, 'Restaurante Sabor & Arte', 'Av. Paulista, 900', 'São Paulo', 'SP', '01310-100', 'Brasil');

-- 8. DETALHES_PEDIDO
INSERT INTO detalhes_pedido (pedido_id, produto_id, preco_unitario, quantidade, desconto) VALUES 
(101, 1, 15.50, 10, 0.05),
(101, 5, 85.00, 2, 0.0),
(102, 9, 48.00, 5, 0.10);