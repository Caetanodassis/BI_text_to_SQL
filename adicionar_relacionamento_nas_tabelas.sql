-- ==============================================================================
-- PARTE 1: CRIANDO AS CHAVES PRIMÁRIAS (PK)
-- ==============================================================================

ALTER TABLE clientes ADD PRIMARY KEY (customer_id);
ALTER TABLE pedidos ADD PRIMARY KEY (order_id);
ALTER TABLE produtos ADD PRIMARY KEY (product_id);
ALTER TABLE vendedores ADD PRIMARY KEY (seller_id);
ALTER TABLE traducao_categoria ADD PRIMARY KEY (product_category_name);
ALTER TABLE itens_pedido ADD PRIMARY KEY (order_id, order_item_id);
ALTER TABLE pagamentos_pedido ADD PRIMARY KEY (order_id, payment_sequential);
ALTER TABLE avaliacoes_pedido ADD PRIMARY KEY (review_id, order_id);


-- ==============================================================================
-- PARTE 2: CORREÇÃO DE DADOS (Tratando as categorias faltantes do dataset Olist)
-- ==============================================================================

-- Insere a categoria pc_gamer (se ela já existir, o ON CONFLICT ignora e segue em frente)
INSERT INTO traducao_categoria (product_category_name, product_category_name_english)
VALUES ('pc_gamer', 'pc_gamer')
ON CONFLICT (product_category_name) DO NOTHING;

-- Insere outra categoria que historicamente também vem faltando nesse dataset
INSERT INTO traducao_categoria (product_category_name, product_category_name_english)
VALUES ('portateis_cozinha_e_preparadores_de_alimentos', 'portable_kitchen_food_preparers')
ON CONFLICT (product_category_name) DO NOTHING;


-- ==============================================================================
-- PARTE 3: CRIANDO AS CHAVES ESTRANGEIRAS (FK - Relacionamentos)
-- ==============================================================================

-- Ligando os Pedidos aos Clientes
ALTER TABLE pedidos 
ADD CONSTRAINT fk_pedidos_clientes 
FOREIGN KEY (customer_id) REFERENCES clientes(customer_id);

-- Ligando os Itens do Pedido aos Pedidos, Produtos e Vendedores
ALTER TABLE itens_pedido 
ADD CONSTRAINT fk_itens_pedidos 
FOREIGN KEY (order_id) REFERENCES pedidos(order_id);

ALTER TABLE itens_pedido 
ADD CONSTRAINT fk_itens_produtos 
FOREIGN KEY (product_id) REFERENCES produtos(product_id);

ALTER TABLE itens_pedido 
ADD CONSTRAINT fk_itens_vendedores 
FOREIGN KEY (seller_id) REFERENCES vendedores(seller_id);

-- Ligando os Pagamentos aos Pedidos
ALTER TABLE pagamentos_pedido 
ADD CONSTRAINT fk_pagamentos_pedidos 
FOREIGN KEY (order_id) REFERENCES pedidos(order_id);

-- Ligando as Avaliações aos Pedidos
ALTER TABLE avaliacoes_pedido 
ADD CONSTRAINT fk_avaliacoes_pedidos 
FOREIGN KEY (order_id) REFERENCES pedidos(order_id);

-- Ligando os Produtos à Tradução de Categorias
ALTER TABLE produtos 
ADD CONSTRAINT fk_produtos_traducao 
FOREIGN KEY (product_category_name) REFERENCES traducao_categoria(product_category_name);