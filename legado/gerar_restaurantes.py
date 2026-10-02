#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para gerar lista completa de restaurantes com dados detalhados
"""
import json

# Dados carregados da pesquisa gastronômica (7 por categoria)
restaurantes_data = {
  "Fondue": [
    {"nome": "Matterhorn", "nota": 4.5, "preco": "$$", "valor_medio": "R$ 120 - R$ 180", "endereco": "Rua Felicíssimo, 145 - Capivari", "tags": ["romantico", "fondue", "vista"], "descricao": "Tradicional restaurante de fondue com ambiente aconchegante à moda suíça."},
    {"nome": "Só Queijo", "nota": 4.6, "preco": "$$$", "valor_medio": "R$ 140 - R$ 220", "endereco": "Av. Macedo Soares, 287 - Capivari", "tags": ["romantico", "fondue", "família"], "descricao": "Especializado em fondue de queijo com seleção premium de queijos europeus."},
    {"nome": "Ludwig Restaurant", "nota": 4.7, "preco": "$$$$", "valor_medio": "R$ 180 - R$ 280", "endereco": "Rua Ernesto Dibert, 52 - Capivari", "tags": ["romantico", "fondue", "vista", "sofisticado"], "descricao": "Requintado restaurante de fondue com vista para a serra."},
    {"nome": "Restaurante Só Queijo (Tradicional)", "nota": 4.4, "preco": "$$", "valor_medio": "R$ 110 - R$ 170", "endereco": "Av. Macedo Soares, 642 - Capivari", "tags": ["fondue", "tradicional"], "descricao": "Um dos clássicos da cidade para fondues variados."},
    {"nome": "Fondue Me", "nota": 4.3, "preco": "$$", "valor_medio": "R$ 100 - R$ 160", "endereco": "Av. Januário Miraglia, 1000 - Abernéssia", "tags": ["fondue"], "descricao": "Ambiente descontraído e ótimo custo-benefício em fondue."},
    {"nome": "Chateau de la Fondue", "nota": 4.5, "preco": "$$$", "valor_medio": "R$ 150 - R$ 210", "endereco": "Rua Djalma Forjaz, 93 - Capivari", "tags": ["fondue", "sofisticado"], "descricao": "Fondue sofisticado no coração do agito de Capivari."},
    {"nome": "Baden Baden Fondue", "nota": 4.2, "preco": "$$$", "valor_medio": "R$ 150 - R$ 210", "endereco": "Rua Djalma Forjaz, 93 - Capivari", "tags": ["fondue", "cervejaria", "amigos"], "descricao": "A experiência do famoso Baden Baden voltada para o fondue."}
  ],
  "Pizzaria": [
    {"nome": "Pizzaria Arte da Pizza", "nota": 4.5, "preco": "$$", "valor_medio": "R$ 80 - R$ 130", "endereco": "Av. Macedo Soares, 218 - Capivari", "tags": ["família", "pizza", "casual"], "descricao": "Pizzas artesanais de fermentação natural em ambiente acolhedor."},
    {"nome": "Pizza do André", "nota": 4.4, "preco": "$$", "valor_medio": "R$ 70 - R$ 120", "endereco": "Av. Dr. Januário Miraglia, 2500 - Abernéssia", "tags": ["família", "pizza"], "descricao": "Opção popular com grande variedade de sabores."},
    {"nome": "Pizzaria Sans Souci", "nota": 4.6, "preco": "$$$", "valor_medio": "R$ 90 - R$ 150", "endereco": "Av. Dr. Januário Miraglia, 3033", "tags": ["família", "pizza", "gourmet"], "descricao": "Pizza gourmet com ingredientes frescos e massa fina."},
    {"nome": "Vila Gourmet Pizza", "nota": 4.3, "preco": "$$", "valor_medio": "R$ 75 - R$ 125", "endereco": "Rua Eng. Diogo de Carvalho, 99 - Capivari", "tags": ["pizza", "casual"], "descricao": "Local central com bom atendimento e pizzas tradicionais."},
    {"nome": "La Fabbrica di Pizza", "nota": 4.2, "preco": "$$", "valor_medio": "R$ 85 - R$ 140", "endereco": "Av. Emílio Ribas, 600 - Capivari", "tags": ["pizza", "italiano"], "descricao": "Pizza no estilo napolitano com forno a lenha."},
    {"nome": "Forneria Campos", "nota": 4.5, "preco": "$$$", "valor_medio": "R$ 100 - R$ 160", "endereco": "Av. Macedo Soares, 500", "tags": ["pizza", "italiano", "sofisticado"], "descricao": "Focada em culinária italiana de forno, excelente pizza."},
    {"nome": "Pizza na Pedra", "nota": 4.1, "preco": "$$", "valor_medio": "R$ 60 - R$ 110", "endereco": "Av. Pedro Paulo, 120", "tags": ["pizza", "casual"], "descricao": "Conceito diferenciado de assar a pizza diretamente na pedra."}
  ],
  "Carnes": [
    {"nome": "Restaurante Libertango", "nota": 4.7, "preco": "$$$", "valor_medio": "R$ 150 - R$ 250", "endereco": "Rua Djalma Forjaz, 175 - Capivari", "tags": ["carnes", "parrilla", "amigos"], "descricao": "Carnes nobres ao estilo argentino com excelente adega."},
    {"nome": "Harry Pisek", "nota": 4.6, "preco": "$$", "valor_medio": "R$ 90 - R$ 150", "endereco": "Rua Wanderley de Araújo, 350", "tags": ["carnes", "tradicional"], "descricao": "Famoso pelas carnes curadas, salsichas artesanais e cortes de porco."},
    {"nome": "Festival da Carne", "nota": 4.3, "preco": "$$", "valor_medio": "R$ 100 - R$ 170", "endereco": "Av. Emílio Ribas, 300", "tags": ["carnes", "família"], "descricao": "Rodízio de carnes com cortes variados."},
    {"nome": "Restaurante Pontremoli", "nota": 4.8, "preco": "$$$$", "valor_medio": "R$ 200 - R$ 350", "endereco": "Rua das Araucárias, 150", "tags": ["carnes", "romantico", "sofisticado"], "descricao": "Cozinha sofisticada com foco em carnes e experiência à luz de velas."},
    {"nome": "Krokodillo", "nota": 4.4, "preco": "$$$", "valor_medio": "R$ 120 - R$ 200", "endereco": "Av. Macedo Soares, 800", "tags": ["carnes", "família"], "descricao": "Grill variado com foco em cortes de carne de alta qualidade."},
    {"nome": "Restaurante Rost", "nota": 4.5, "preco": "$$$", "valor_medio": "R$ 130 - R$ 210", "endereco": "Av. Dr. Januário Miraglia, 2000", "tags": ["carnes", "sofisticado"], "descricao": "Cozinha contemporânea com excelente seleção de carnes grelhadas."},
    {"nome": "Campos Grill", "nota": 4.2, "preco": "$$", "valor_medio": "R$ 80 - R$ 140", "endereco": "Av. Emílio Ribas, 450", "tags": ["carnes", "casual"], "descricao": "Carnes na brasa e pratos rápidos em ambiente informal."}
  ],
  "Cervejaria": [
    {"nome": "Baden Baden", "nota": 4.6, "preco": "$$$", "valor_medio": "R$ 100 - R$ 200", "endereco": "Rua Djalma Forjaz, 93 - Capivari", "tags": ["cervejaria", "amigos", "tradicional"], "descricao": "O clássico cervejaria da cidade, obrigatório para os amantes de cerveja artesanal."},
    {"nome": "Caroli", "nota": 4.3, "preco": "$$", "valor_medio": "R$ 70 - R$ 120", "endereco": "Av. Macedo Soares, 250", "tags": ["cervejaria", "amigos", "casual"], "descricao": "Pub focado em chopes artesanais locais e petiscos."},
    {"nome": "Cervejaria Campos do Jordão", "nota": 4.5, "preco": "$$$", "valor_medio": "R$ 90 - R$ 160", "endereco": "Av. Dr. Januário Miraglia, 1500", "tags": ["cervejaria", "amigos", "vista"], "descricao": "Local de produção própria com um amplo deck e excelente comida."},
    {"nome": "Bar do Bolinho", "nota": 4.2, "preco": "$", "valor_medio": "R$ 50 - R$ 90", "endereco": "Rua Djalma Forjaz, 50", "tags": ["cervejaria", "casual"], "descricao": "Ideal para petiscos e chope gelado com ambiente descontraído."},
    {"nome": "Vila Beer", "nota": 4.4, "preco": "$$", "valor_medio": "R$ 60 - R$ 110", "endereco": "Av. Emílio Ribas, 500", "tags": ["cervejaria", "amigos"], "descricao": "Variedade de rótulos artesanais e música ao vivo."},
    {"nome": "Pub 1920", "nota": 4.3, "preco": "$$", "valor_medio": "R$ 70 - R$ 130", "endereco": "Rua Djalma Forjaz, 110", "tags": ["cervejaria", "amigos"], "descricao": "Pub temático com foco em cervejas especiais e drinques."},
    {"nome": "Cervejaria do Horto", "nota": 4.6, "preco": "$$", "valor_medio": "R$ 80 - R$ 140", "endereco": "Estrada do Horto Florestal", "tags": ["cervejaria", "natureza"], "descricao": "Ambiente integrado à natureza com chopes exclusivos."}
  ],
  "Cafés": [
    {"nome": "Chocolate Montanhês", "nota": 4.5, "preco": "$$", "valor_medio": "R$ 40 - R$ 80", "endereco": "Rua Djalma Forjaz, 150", "tags": ["cafés", "tradicional"], "descricao": "Café, chocolate quente cremoso e tortas irresistíveis."},
    {"nome": "Sans Souci Bistro", "nota": 4.7, "preco": "$$$", "valor_medio": "R$ 60 - R$ 120", "endereco": "Av. Dr. Januário Miraglia, 3033", "tags": ["cafés", "sofisticado"], "descricao": "Café da manhã de luxo e confeitaria fina em ambiente bucólico."},
    {"nome": "Café Terraço", "nota": 4.4, "preco": "$$", "valor_medio": "R$ 50 - R$ 90", "endereco": "Av. Macedo Soares, 100", "tags": ["cafés", "vista"], "descricao": "Ótima vista para o movimento de Capivari."},
    {"nome": "Spinassi Chocolate", "nota": 4.6, "preco": "$$", "valor_medio": "R$ 40 - R$ 70", "endereco": "Av. Macedo Soares, 200", "tags": ["cafés", "tradicional"], "descricao": "Conhecido pelo chocolate quente artesanal e doces típicos."},
    {"nome": "Le Bon Café", "nota": 4.3, "preco": "$$", "valor_medio": "R$ 30 - R$ 60", "endereco": "Rua Eng. Diogo de Carvalho, 150", "tags": ["cafés", "casual"], "descricao": "Café aconchegante, ideal para um descanso durante o passeio."},
    {"nome": "Confeitaria Itália", "nota": 4.2, "preco": "$$", "valor_medio": "R$ 35 - R$ 70", "endereco": "Av. Emílio Ribas, 400", "tags": ["cafés", "italiano"], "descricao": "Tortas, salgados e cafés com estilo europeu."},
    {"nome": "Café do Zé", "nota": 4.1, "preco": "$", "valor_medio": "R$ 20 - R$ 50", "endereco": "Av. Dr. Januário Miraglia, 800", "tags": ["cafés", "casual"], "descricao": "Café simples e direto, excelente custo-benefício."}
  ]
}

def gerar():
    lista_completa = []
    for categoria, lista in restaurantes_data.items():
        for r in lista:
            r['categoria'] = categoria
            r['subcategoria'] = categoria
            r.setdefault('maps', f"https://www.google.com/search?q={r['nome'].replace(' ', '+')}+Campos+do+Jordao")
            lista_completa.append(r)
    
    with open('restaurantes.json', 'w', encoding='utf-8') as f:
        json.dump(lista_completa, f, indent=2, ensure_ascii=False)

if __name__ == '__main__':
    gerar()
