-- =====================================================================
-- Qorvus - V002: Dados de teste (loja de cabelo, maquiagem e beleza)
-- Rodar DEPOIS do V001.
-- Você pode usar qualquer dado de teste, usei esse script apenas de exemplo.

USE qorvus;
-- empresa

INSERT INTO empresa (nome_empresa, cnpj)
VALUES ('Bella Vitta Cosméticos LTDA', '12345678000195');

SET @empresa := (SELECT id FROM empresa WHERE cnpj = '12345678000195');

-- usuario

INSERT INTO usuario (
nome_completo, cpf, cargo, data_admissao, empresa_id, email, telefone, senha_hash, perfil, status_ativo
) VALUES
('Marina Albuquerque Costa', '00000000101', 'ADMINISTRADOR', '2022-03-01', @empresa, 'marina@bellavitta.com.br', '(11) 90000-0001', '2b10HASH_FICTICIO', 'ADMINISTRADOR', TRUE),
('Carlos Eduardo Pinheiro',  '00000000202', 'FUNCIONARIO',   '2023-06-15', @empresa, 'carlos@bellavitta.com.br',  '(11) 90000-0002', '$2b$10HASH_FICTICIO', 'FUNCIONARIO',   TRUE),
('Juliana Ribeiro Matos',    '00000000303', 'FUNCIONARIO',   '2024-01-10', @empresa, 'juliana@bellavitta.com.br', '(11) 90000-0003', '2b10HASH_FICTICIO', 'FUNCIONARIO',   TRUE),
('Rafael Nogueira Lima',     '00000000404', 'FUNCIONARIO',   '2021-09-20', @empresa, 'rafael@bellavitta.com.br',  '(11) 90000-0004', '$2b$10HASH_FICTICIO', 'FUNCIONARIO',   FALSE);

-- categoria

INSERT INTO categoria (empresa_id, nome, descricao, status_ativo) VALUES
(@empresa, 'Shampoo e Condicionador', 'Limpeza e hidratação diária dos cabelos', TRUE),
(@empresa, 'Tratamento Capilar',      'Máscaras, óleos e reconstrução capilar', TRUE),
(@empresa, 'Finalizadores',           'Leave-in, cremes de pentear e ativadores de cachos', TRUE),
(@empresa, 'Maquiagem Rosto',         'Bases, corretivos, pós, blushes e iluminadores', TRUE),
(@empresa, 'Maquiagem Olhos',         'Máscaras de cílios, sombras e delineadores', TRUE),
(@empresa, 'Maquiagem Lábios',        'Batons e glosses', TRUE),
(@empresa, 'Skincare',                'Cuidados com a pele do rosto e do corpo', TRUE),
(@empresa, 'Perfumaria',              'Perfumes e body splashes', TRUE),
(@empresa, 'Unhas',                   'Esmaltes e acessórios para unhas', TRUE),
(@empresa, 'Acessórios',              'Pincéis, esponjas e aparelhos para cabelo', TRUE),
(@empresa, 'Kits Promocionais',       'Categoria desativada para testes de filtro', FALSE);

-- marca

INSERT INTO marca (empresa_id, nome, descricao, status_ativo) VALUES
(@empresa, 'L''Oréal Paris',   'Cuidados capilares e maquiagem', TRUE),
(@empresa, 'Pantene',          'Linha de tratamento capilar', TRUE),
(@empresa, 'Seda',             'Shampoos, condicionadores e finalizadores', TRUE),
(@empresa, 'Salon Line',       'Cosméticos capilares, foco em cachos', TRUE),
(@empresa, 'Maybelline',       'Maquiagem de rosto, olhos e lábios', TRUE),
(@empresa, 'Vult',             'Maquiagem nacional de uso diário', TRUE),
(@empresa, 'Ruby Rose',        'Maquiagem com bom custo-benefício', TRUE),
(@empresa, 'Dailus',           'Maquiagem nacional', TRUE),
(@empresa, 'Garnier',          'Skincare e cuidados capilares', TRUE),
(@empresa, 'La Roche-Posay',   'Dermocosméticos e proteção solar', TRUE),
(@empresa, 'Nivea',            'Hidratação e cuidados com a pele', TRUE),
(@empresa, 'Natura',           'Perfumaria e cuidados corporais', TRUE),
(@empresa, 'O Boticário',      'Perfumaria e maquiagem', TRUE),
(@empresa, 'Risqué',           'Esmaltes', TRUE),
(@empresa, 'Colorama',         'Esmaltes', TRUE),
(@empresa, 'Taiff',            'Aparelhos profissionais para cabelo', TRUE),
(@empresa, 'Beleza Antiga',    'Marca descontinuada, usada para testes de filtro', FALSE);

-- Variáveis auxiliares (IDs das categorias e marcas)

SET @c_shampoo := (SELECT id FROM categoria WHERE nome = 'Shampoo e Condicionador');
SET @c_trat    := (SELECT id FROM categoria WHERE nome = 'Tratamento Capilar');
SET @c_final   := (SELECT id FROM categoria WHERE nome = 'Finalizadores');
SET @c_rosto   := (SELECT id FROM categoria WHERE nome = 'Maquiagem Rosto');
SET @c_olhos   := (SELECT id FROM categoria WHERE nome = 'Maquiagem Olhos');
SET @c_labios  := (SELECT id FROM categoria WHERE nome = 'Maquiagem Lábios');
SET @c_skin    := (SELECT id FROM categoria WHERE nome = 'Skincare');
SET @c_perf    := (SELECT id FROM categoria WHERE nome = 'Perfumaria');
SET @c_unhas   := (SELECT id FROM categoria WHERE nome = 'Unhas');
SET @c_acess   := (SELECT id FROM categoria WHERE nome = 'Acessórios');

SET @m_loreal  := (SELECT id FROM marca WHERE nome = 'L''Oréal Paris');
SET @m_pantene := (SELECT id FROM marca WHERE nome = 'Pantene');
SET @m_seda    := (SELECT id FROM marca WHERE nome = 'Seda');
SET @m_salon   := (SELECT id FROM marca WHERE nome = 'Salon Line');
SET @m_maybel  := (SELECT id FROM marca WHERE nome = 'Maybelline');
SET @m_vult    := (SELECT id FROM marca WHERE nome = 'Vult');
SET @m_ruby    := (SELECT id FROM marca WHERE nome = 'Ruby Rose');
SET @m_dailus  := (SELECT id FROM marca WHERE nome = 'Dailus');
SET @m_garnier := (SELECT id FROM marca WHERE nome = 'Garnier');
SET @m_lrp     := (SELECT id FROM marca WHERE nome = 'La Roche-Posay');
SET @m_nivea   := (SELECT id FROM marca WHERE nome = 'Nivea');
SET @m_natura  := (SELECT id FROM marca WHERE nome = 'Natura');
SET @m_boti    := (SELECT id FROM marca WHERE nome = 'O Boticário');
SET @m_risque  := (SELECT id FROM marca WHERE nome = 'Risqué');
SET @m_colo    := (SELECT id FROM marca WHERE nome = 'Colorama');
SET @m_taiff   := (SELECT id FROM marca WHERE nome = 'Taiff');

-- item

INSERT INTO item (
empresa_id, nome, quantidade, categoria_id, marca_id, preco_venda, preco_custo, limite_minimo, status_removido, descricao, imagem_item
) VALUES
(@empresa, 'Shampoo Elseve Reparação Total 5 400ml',              48, @c_shampoo, @m_loreal,  21.90,  12.50, 10, FALSE, 'Shampoo para cabelos danificados', 'imagens/itens/elseve-shampoo-rt5.jpg'),
(@empresa, 'Condicionador Elseve Reparação Total 5 400ml',        45, @c_shampoo, @m_loreal,  21.90,  12.50, 10, FALSE, 'Condicionador para cabelos danificados', 'imagens/itens/elseve-cond-rt5.jpg'),
(@empresa, 'Shampoo Pantene Hidro-Cauterização 400ml',            40, @c_shampoo, @m_pantene, 24.90,  14.00, 10, FALSE, 'Hidratação e reparação dos fios', 'imagens/itens/pantene-hidro-shampoo.jpg'),
(@empresa, 'Shampoo Seda Ceramidas 325ml',                        36, @c_shampoo, @m_seda,    14.90,   7.50, 10, FALSE, 'Shampoo com ceramidas para força e brilho', 'imagens/itens/seda-ceramidas.jpg'),
(@empresa, 'Máscara Elseve Reparação Total 5 300g',               22, @c_trat,    @m_loreal,  32.90,  18.00,  8, FALSE, 'Tratamento intensivo para cabelos danificados', 'imagens/itens/elseve-mascara-rt5.jpg'),
(@empresa, 'Óleo Elseve Óleo Extraordinário 100ml',               26, @c_trat,    @m_loreal,  44.90,  25.00,  8, FALSE, 'Óleo nutritivo para brilho e maciez', 'imagens/itens/elseve-oleo.jpg'),
(@empresa, 'Ativador de Cachos Salon Line #TodeCacho 300ml',       4, @c_final,   @m_salon,   19.90,  10.50,  8, FALSE, 'Definição e hidratação para cachos', 'imagens/itens/salonline-todecacho.jpg'),
(@empresa, 'Creme para Pentear Seda Cachos Definidos 250ml',      30, @c_final,   @m_seda,    16.90,   8.50,  8, FALSE, 'Creme para pentear cabelos cacheados', 'imagens/itens/seda-creme-cachos.jpg'),
(@empresa, 'Secador de Cabelo Taiff Style 1900W',                 12, @c_acess,   @m_taiff,  189.90, 115.00,  4, FALSE, 'Secador com potência de 1900W', 'imagens/itens/taiff-style.jpg'),
(@empresa, 'Base Líquida Maybelline Fit Me Matte Poreless Tom 120', 35, @c_rosto, @m_maybel,  54.90,  32.00, 10, FALSE, 'Base com acabamento matte', 'imagens/itens/fitme-120.jpg'),
(@empresa, 'Base Líquida Maybelline Fit Me Matte Poreless Tom 220', 28, @c_rosto, @m_maybel,  54.90,  32.00, 10, FALSE, 'Base com acabamento matte', 'imagens/itens/fitme-220.jpg'),
(@empresa, 'Corretivo Maybelline Instant Age Rewind',             40, @c_rosto,   @m_maybel,  49.90,  28.00, 10, FALSE, 'Corretivo para olheiras e imperfeições', 'imagens/itens/age-rewind.jpg'),
(@empresa, 'Pó Compacto Vult Make Up',                            28, @c_rosto,   @m_vult,    19.90,  10.00,  8, FALSE, 'Controle de brilho com acabamento suave', 'imagens/itens/vult-po-compacto.jpg'),
(@empresa, 'Blush Compacto Dailus Rosé',                          25, @c_rosto,   @m_dailus,  24.90,  13.00,  8, FALSE, 'Cor natural e fácil de esfumar', 'imagens/itens/dailus-blush.jpg'),
(@empresa, 'Iluminador Líquido Melu by Ruby Rose',                 8, @c_rosto,   @m_ruby,    29.90,  15.00,  5, FALSE, 'Brilho suave para pontos de luz do rosto', 'imagens/itens/melu-iluminador.jpg'),
(@empresa, 'Máscara de Cílios Maybelline Lash Sensational',       50, @c_olhos,   @m_maybel,  54.90,  30.00, 12, FALSE, 'Volume e definição para os cílios', 'imagens/itens/lash-sensational.jpg'),
(@empresa, 'Paleta de Sombras Vult Nude',                         13, @c_olhos,   @m_vult,    39.90,  21.00,  5, FALSE, 'Tons nude foscos e cintilantes', 'imagens/itens/vult-paleta-nude.jpg'),
(@empresa, 'Delineador Líquido Vult Make Up Preto',               44, @c_olhos,   @m_vult,    17.90,   9.00, 10, FALSE, 'Ponta fina para traço preciso', 'imagens/itens/vult-delineador.jpg'),
(@empresa, 'Batom Maybelline Color Sensational Vermelho',         38, @c_labios,  @m_maybel,  39.90,  22.00, 10, FALSE, 'Cor intensa com acabamento cremoso', 'imagens/itens/color-sensational-vermelho.jpg'),
(@empresa, 'Batom Ruby Rose Matte Nude',                          41, @c_labios,  @m_ruby,    22.90,  11.50, 10, FALSE, 'Acabamento matte de longa duração', 'imagens/itens/ruby-rose-matte-nude.jpg'),
(@empresa, 'Gloss Labial Maybelline Lifter Gloss',                 3, @c_labios,  @m_maybel,  59.90,  34.00,  8, FALSE, 'Brilho e hidratação para os lábios', 'imagens/itens/lifter-gloss.jpg'),
(@empresa, 'Protetor Solar Facial La Roche-Posay Anthelios FPS 60', 20, @c_skin,  @m_lrp,     89.90,  58.00,  6, FALSE, 'Proteção solar facial de alta proteção', 'imagens/itens/anthelios-fps60.jpg'),
(@empresa, 'Água Micelar Garnier Solução Micelar 5 em 1 400ml',   36, @c_skin,    @m_garnier, 34.90,  19.00, 10, FALSE, 'Remove maquiagem e limpa a pele', 'imagens/itens/garnier-micelar.jpg'),
(@empresa, 'Hidratante Nivea Creme Lata 145g',                    27, @c_skin,    @m_nivea,   19.90,  11.00,  8, FALSE, 'Creme hidratante para rosto e corpo', 'imagens/itens/nivea-creme.jpg'),
(@empresa, 'Lily Eau de Parfum 75ml',                             12, @c_perf,    @m_boti,   249.90, 150.00,  4, FALSE, 'Perfume feminino de notas florais', 'imagens/itens/boti-lily.jpg'),
(@empresa, 'Body Splash Natura Tododia Macadâmia 200ml',          24, @c_perf,    @m_natura,  54.90,  30.00,  6, FALSE, 'Fragrância corporal suave e refrescante', 'imagens/itens/natura-tododia-macadamia.jpg'),
(@empresa, 'Esmalte Risqué Cremoso 8ml Vermelho',                 60, @c_unhas,   @m_risque,   4.90,   2.20, 15, FALSE, 'Esmalte cremoso vermelho', 'imagens/itens/risque-vermelho.jpg'),
(@empresa, 'Esmalte Colorama 8ml Rosa',                           55, @c_unhas,   @m_colo,     3.90,   1.80, 15, FALSE, 'Esmalte rosa de secagem rápida', 'imagens/itens/colorama-rosa.jpg'),
(@empresa, 'Kit Pincéis de Maquiagem 10 peças',                   18, @c_acess,   NULL,       79.90,  40.00,  5, FALSE, 'Kit completo com estojo', 'imagens/itens/kit-pinceis.jpg'),
(@empresa, 'Esponja de Maquiagem Gota',                            0, @c_acess,   NULL,       14.90,   6.00, 10, TRUE,  'Item descontinuado (removido do catálogo)', NULL);

-- movimentacao

SET @u_marina  := (SELECT id FROM usuario WHERE email = 'marina@bellavitta.com.br');
SET @u_carlos  := (SELECT id FROM usuario WHERE email = 'carlos@bellavitta.com.br');
SET @u_juliana := (SELECT id FROM usuario WHERE email = 'juliana@bellavitta.com.br');
SET @u_rafael  := (SELECT id FROM usuario WHERE email = 'rafael@bellavitta.com.br');

INSERT INTO movimentacao (empresa_id, item_id, usuario_id, tipo, quantidade, data_hora) VALUES
(@empresa, (SELECT id FROM item WHERE nome = 'Shampoo Elseve Reparação Total 5 400ml'),              @u_carlos,  'ENTRADA', 38, '2026-08-03 10:07:00'),
(@empresa, (SELECT id FROM item WHERE nome = 'Shampoo Elseve Reparação Total 5 400ml'),              @u_carlos,  'SAIDA',    6, '2026-09-03 10:10:00'),
(@empresa, (SELECT id FROM item WHERE nome = 'Shampoo Elseve Reparação Total 5 400ml'),              @u_juliana, 'SAIDA',    4, '2026-09-20 15:30:00'),
(@empresa, (SELECT id FROM item WHERE nome = 'Shampoo Elseve Reparação Total 5 400ml'),              @u_marina,  'ENTRADA', 20, '2026-09-22 09:30:00'),
(@empresa, (SELECT id FROM item WHERE nome = 'Condicionador Elseve Reparação Total 5 400ml'),        @u_juliana, 'ENTRADA', 50, '2026-08-03 11:14:00'),
(@empresa, (SELECT id FROM item WHERE nome = 'Condicionador Elseve Reparação Total 5 400ml'),        @u_carlos,  'SAIDA',    5, '2026-09-03 10:20:00'),
(@empresa, (SELECT id FROM item WHERE nome = 'Shampoo Pantene Hidro-Cauterização 400ml'),            @u_marina,  'ENTRADA', 40, '2026-08-03 12:21:00'),
(@empresa, (SELECT id FROM item WHERE nome = 'Shampoo Seda Ceramidas 325ml'),                        @u_carlos,  'ENTRADA', 39, '2026-08-04 09:28:00'),
(@empresa, (SELECT id FROM item WHERE nome = 'Shampoo Seda Ceramidas 325ml'),                        @u_juliana, 'SAIDA',    3, '2026-09-10 11:45:00'),
(@empresa, (SELECT id FROM item WHERE nome = 'Máscara Elseve Reparação Total 5 300g'),               @u_juliana, 'ENTRADA', 22, '2026-08-04 10:35:00'),
(@empresa, (SELECT id FROM item WHERE nome = 'Óleo Elseve Óleo Extraordinário 100ml'),               @u_marina,  'ENTRADA', 30, '2026-08-04 11:42:00'),
(@empresa, (SELECT id FROM item WHERE nome = 'Óleo Elseve Óleo Extraordinário 100ml'),               @u_carlos,  'SAIDA',    4, '2026-09-12 14:15:00'),
(@empresa, (SELECT id FROM item WHERE nome = 'Ativador de Cachos Salon Line #TodeCacho 300ml'),       @u_carlos,  'ENTRADA', 13, '2026-08-05 12:49:00'),
(@empresa, (SELECT id FROM item WHERE nome = 'Ativador de Cachos Salon Line #TodeCacho 300ml'),       @u_carlos,  'SAIDA',    6, '2026-09-02 17:20:00'),
(@empresa, (SELECT id FROM item WHERE nome = 'Ativador de Cachos Salon Line #TodeCacho 300ml'),       @u_juliana, 'SAIDA',    3, '2026-09-16 09:40:00'),
(@empresa, (SELECT id FROM item WHERE nome = 'Creme para Pentear Seda Cachos Definidos 250ml'),      @u_juliana, 'ENTRADA', 30, '2026-08-05 09:56:00'),
(@empresa, (SELECT id FROM item WHERE nome = 'Secador de Cabelo Taiff Style 1900W'),                 @u_marina,  'ENTRADA', 13, '2026-08-05 10:03:00'),
(@empresa, (SELECT id FROM item WHERE nome = 'Secador de Cabelo Taiff Style 1900W'),                 @u_marina,  'SAIDA',    1, '2026-09-14 16:00:00'),
(@empresa, (SELECT id FROM item WHERE nome = 'Base Líquida Maybelline Fit Me Matte Poreless Tom 120'), @u_carlos,  'ENTRADA', 40, '2026-08-06 11:10:00'),
(@empresa, (SELECT id FROM item WHERE nome = 'Base Líquida Maybelline Fit Me Matte Poreless Tom 120'), @u_juliana, 'SAIDA',    5, '2026-09-06 13:20:00'),
(@empresa, (SELECT id FROM item WHERE nome = 'Base Líquida Maybelline Fit Me Matte Poreless Tom 220'), @u_juliana, 'ENTRADA', 28, '2026-08-06 12:17:00'),
(@empresa, (SELECT id FROM item WHERE nome = 'Corretivo Maybelline Instant Age Rewind'),             @u_marina,  'ENTRADA', 48, '2026-08-06 09:24:00'),
(@empresa, (SELECT id FROM item WHERE nome = 'Corretivo Maybelline Instant Age Rewind'),             @u_carlos,  'SAIDA',    8, '2026-09-09 12:05:00'),
(@empresa, (SELECT id FROM item WHERE nome = 'Pó Compacto Vult Make Up'),                            @u_carlos,  'ENTRADA', 33, '2026-08-07 10:31:00'),
(@empresa, (SELECT id FROM item WHERE nome = 'Pó Compacto Vult Make Up'),                            @u_rafael,  'SAIDA',    5, '2026-09-17 16:55:00'),
(@empresa, (SELECT id FROM item WHERE nome = 'Blush Compacto Dailus Rosé'),                          @u_juliana, 'ENTRADA', 25, '2026-08-07 11:38:00'),
(@empresa, (SELECT id FROM item WHERE nome = 'Iluminador Líquido Melu by Ruby Rose'),                 @u_marina,  'ENTRADA', 12, '2026-08-07 12:45:00'),
(@empresa, (SELECT id FROM item WHERE nome = 'Iluminador Líquido Melu by Ruby Rose'),                 @u_carlos,  'SAIDA',    4, '2026-09-08 10:05:00'),
(@empresa, (SELECT id FROM item WHERE nome = 'Máscara de Cílios Maybelline Lash Sensational'),       @u_carlos,  'ENTRADA', 54, '2026-08-08 09:52:00'),
(@empresa, (SELECT id FROM item WHERE nome = 'Máscara de Cílios Maybelline Lash Sensational'),       @u_juliana, 'SAIDA',   10, '2026-09-05 11:30:00'),
(@empresa, (SELECT id FROM item WHERE nome = 'Máscara de Cílios Maybelline Lash Sensational'),       @u_carlos,  'SAIDA',    6, '2026-09-18 17:10:00'),
(@empresa, (SELECT id FROM item WHERE nome = 'Máscara de Cílios Maybelline Lash Sensational'),       @u_juliana, 'ENTRADA', 12, '2026-09-23 10:00:00'),
(@empresa, (SELECT id FROM item WHERE nome = 'Paleta de Sombras Vult Nude'),                         @u_juliana, 'ENTRADA', 16, '2026-08-08 10:59:00'),
(@empresa, (SELECT id FROM item WHERE nome = 'Paleta de Sombras Vult Nude'),                         @u_juliana, 'SAIDA',    3, '2026-09-11 18:00:00'),
(@empresa, (SELECT id FROM item WHERE nome = 'Delineador Líquido Vult Make Up Preto'),               @u_marina,  'ENTRADA', 44, '2026-08-08 11:06:00'),
(@empresa, (SELECT id FROM item WHERE nome = 'Batom Maybelline Color Sensational Vermelho'),         @u_carlos,  'ENTRADA', 45, '2026-08-09 12:13:00'),
(@empresa, (SELECT id FROM item WHERE nome = 'Batom Maybelline Color Sensational Vermelho'),         @u_marina,  'SAIDA',    7, '2026-09-13 15:25:00'),
(@empresa, (SELECT id FROM item WHERE nome = 'Batom Ruby Rose Matte Nude'),                          @u_juliana, 'ENTRADA', 41, '2026-08-09 09:20:00'),
(@empresa, (SELECT id FROM item WHERE nome = 'Gloss Labial Maybelline Lifter Gloss'),                 @u_marina,  'ENTRADA', 15, '2026-08-09 10:27:00'),
(@empresa, (SELECT id FROM item WHERE nome = 'Gloss Labial Maybelline Lifter Gloss'),                 @u_juliana, 'SAIDA',    9, '2026-09-04 12:35:00'),
(@empresa, (SELECT id FROM item WHERE nome = 'Gloss Labial Maybelline Lifter Gloss'),                 @u_carlos,  'SAIDA',    3, '2026-09-19 10:50:00'),
(@empresa, (SELECT id FROM item WHERE nome = 'Protetor Solar Facial La Roche-Posay Anthelios FPS 60'), @u_carlos, 'ENTRADA', 22, '2026-08-10 11:34:00'),
(@empresa, (SELECT id FROM item WHERE nome = 'Protetor Solar Facial La Roche-Posay Anthelios FPS 60'), @u_marina, 'SAIDA',    2, '2026-09-15 09:55:00'),
(@empresa, (SELECT id FROM item WHERE nome = 'Água Micelar Garnier Solução Micelar 5 em 1 400ml'),   @u_juliana, 'ENTRADA', 36, '2026-08-10 12:41:00'),
(@empresa, (SELECT id FROM item WHERE nome = 'Hidratante Nivea Creme Lata 145g'),                    @u_marina,  'ENTRADA', 27, '2026-08-10 09:48:00'),
(@empresa, (SELECT id FROM item WHERE nome = 'Lily Eau de Parfum 75ml'),                             @u_carlos,  'ENTRADA', 14, '2026-08-11 10:55:00'),
(@empresa, (SELECT id FROM item WHERE nome = 'Lily Eau de Parfum 75ml'),                             @u_marina,  'SAIDA',    2, '2026-09-15 11:30:00'),
(@empresa, (SELECT id FROM item WHERE nome = 'Body Splash Natura Tododia Macadâmia 200ml'),          @u_juliana, 'ENTRADA', 30, '2026-08-11 11:02:00'),
(@empresa, (SELECT id FROM item WHERE nome = 'Body Splash Natura Tododia Macadâmia 200ml'),          @u_juliana, 'SAIDA',    6, '2026-09-21 14:40:00'),
(@empresa, (SELECT id FROM item WHERE nome = 'Esmalte Risqué Cremoso 8ml Vermelho'),                 @u_marina,  'ENTRADA', 75, '2026-08-11 12:09:00'),
(@empresa, (SELECT id FROM item WHERE nome = 'Esmalte Risqué Cremoso 8ml Vermelho'),                 @u_carlos,  'SAIDA',   15, '2026-09-07 16:20:00'),
(@empresa, (SELECT id FROM item WHERE nome = 'Esmalte Colorama 8ml Rosa'),                           @u_carlos,  'ENTRADA', 55, '2026-08-12 09:16:00'),
(@empresa, (SELECT id FROM item WHERE nome = 'Kit Pincéis de Maquiagem 10 peças'),                   @u_juliana, 'ENTRADA', 18, '2026-08-12 10:23:00');