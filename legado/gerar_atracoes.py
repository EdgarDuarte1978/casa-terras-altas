#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gera atracoes.json — curadoria de atrações de Campos do Jordão e região.

Captura-alvo: de 10 a 15 atrações por categoria (a versão anterior tinha 7).
As categorias e as tags são as mesmas usadas por o_que_fazer.html / script_atracoes.js:
    Natureza -> natureza | Passeios Clássicos -> passeios | Cultura -> cultura
    Compras  -> compras  | Aventura           -> aventura | Mirantes -> mirantes

IMPORTANTE: esta é uma curadoria inicial. Antes de publicar para hóspedes,
confirme endereço exato, horário de funcionamento e se a atração está ativa.
Rode:  py -3 gerar_atracoes.py
"""
import json
from pathlib import Path
from urllib.parse import quote_plus

ROOT = Path(__file__).resolve().parent
JSON_PATH = ROOT / "atracoes.json"

# Faixa de captura desejada por categoria
POR_CATEGORIA_MIN = 10
POR_CATEGORIA_MAX = 15

TAG_POR_CATEGORIA = {
    "Natureza": "natureza",
    "Passeios Clássicos": "passeios",
    "Cultura": "cultura",
    "Compras": "compras",
    "Aventura": "aventura",
    "Mirantes": "mirantes",
}

# ---------------------------------------------------------------------------
# Curadoria (10 a 15 por categoria)
# "tags" aqui é apenas para tags EXTRA além da tag da categoria (ex.: cruzamento
# mirante/aventura). A tag da categoria é adicionada automaticamente em gerar().
# ---------------------------------------------------------------------------
atracoes_data = {
    "Natureza": [
        {"nome": "Parque Amantikir", "nota": 4.8, "endereco": "Estrada Campos do Jordão–Eugênio Lefèvre, km 269", "descricao": "Jardins temáticos inspirados em vários países, com vista privilegiada para a serra."},
        {"nome": "Horto Florestal (Parque Estadual)", "nota": 4.7, "endereco": "Av. Pedro Paulo, s/n - Horto Florestal", "descricao": "Um dos parques mais antigos do país; trilhas, araucárias, rio e piquenique."},
        {"nome": "Bosque do Silêncio", "nota": 4.6, "endereco": "Av. Sen. Roberto Simonsen, 1724", "descricao": "Reserva de mata nativa com trilhas leves e atividades de arvorismo."},
        {"nome": "Represa do Lagoinha", "nota": 4.5, "endereco": "Estrada da Lagoinha, s/n", "descricao": "Área tranquila para caminhadas e contato com a natureza, longe do agito."},
        {"nome": "Borboletário Flores que Voam", "nota": 4.5, "endereco": "Av. Dr. Paulo Ferraz de Camargo, s/n", "descricao": "Espaço de criação e observação de borboletas nativas da Mata Atlântica."},
        {"nome": "Parque dos Elfos", "nota": 4.4, "endereco": "Estrada do Horto Florestal", "descricao": "Bosque temático familiar com casinhas, trilha e atividades ao ar livre."},
        {"nome": "Trilha dos Jesuítas", "nota": 4.6, "endereco": "Parque Estadual - Horto Florestal", "descricao": "Trilha histórica em meio à floresta de araucárias dentro do parque estadual."},
        {"nome": "Cachoeira dos Amores", "nota": 4.6, "endereco": "Parque Estadual - Horto Florestal", "descricao": "Queda d'água acessível por trilha curta a partir do Horto Florestal."},
        {"nome": "Vale das Cachoeiras (Eugênio Lefèvre)", "nota": 4.5, "endereco": "Distrito de Eugênio Lefèvre", "descricao": "Conjunto de cachoeiras e poços em área rural, ótimo para o verão."},
        {"nome": "Poço do Pito", "nota": 4.4, "endereco": "Parque Estadual - Horto Florestal", "descricao": "Poço de águas geladas do rio Sapucaí-Guaçu, dentro do Horto Florestal."},
        {"nome": "Ninho da Águia (área de mata)", "nota": 4.5, "endereco": "Estrada do Ninho da Águia - Alto da Boa Vista", "descricao": "Mata preservada no ponto mais alto da cidade, com mirante natural."},
        {"nome": "Reserva do Trabiju", "nota": 4.4, "endereco": "São Bento do Sapucaí (região)", "descricao": "Área natural de mata e cachoeiras na divisa com São Bento do Sapucaí."},
    ],
    "Passeios Clássicos": [
        {"nome": "Vila Capivari", "nota": 4.8, "endereco": "Av. Macedo Soares - Capivari", "descricao": "O coração turístico da cidade: restaurantes, lojas, chocolaterias e vida noturna."},
        {"nome": "Morro do Elefante", "nota": 4.7, "endereco": "Alto do Morro do Elefante", "descricao": "Ponto clássico com vista panorâmica; acesso por teleférico, carro ou trilha."},
        {"nome": "Teleférico do Morro do Elefante", "nota": 4.6, "endereco": "Parque Capivari", "descricao": "Primeiro teleférico do Brasil, liga o Parque Capivari ao topo do morro."},
        {"nome": "Bondinho / Parque Capivari", "nota": 4.5, "endereco": "Estação Emílio Ribas / Parque Capivari", "descricao": "Parque com lago, pedalinhos, roda-gigante e o embarque do bondinho."},
        {"nome": "Ducha de Prata", "nota": 4.3, "endereco": "Av. Dr. Roberto Simonsen", "descricao": "Quedas d'água em meio à mata, com quiosques de artesanato no entorno."},
        {"nome": "Portal da Cidade", "nota": 4.5, "endereco": "Entrada da cidade - Rod. Floriano Rodrigues Pinheiro", "descricao": "Portal monumental em estilo alpino, parada tradicional para fotos na chegada."},
        {"nome": "Estrada de Ferro Campos do Jordão", "nota": 4.6, "endereco": "Estação Emílio Ribas - Abernéssia", "descricao": "Passeios turísticos de trem pela ferrovia mais alta do Brasil."},
        {"nome": "Lago do Parque Capivari", "nota": 4.4, "endereco": "Parque Capivari", "descricao": "Lago central de Capivari com pedalinhos e cafés à beira d'água."},
        {"nome": "Praça do Capivari", "nota": 4.5, "endereco": "Capivari", "descricao": "Praça arborizada no centro de Capivari, com feirinhas nos fins de semana."},
        {"nome": "Vila Abernéssia", "nota": 4.3, "endereco": "Abernéssia", "descricao": "Centro comercial e histórico da cidade, com o comércio do dia a dia."},
        {"nome": "Passeio de charrete / jardineira", "nota": 4.2, "endereco": "Capivari", "descricao": "City tour tradicional saindo de Capivari pelos principais pontos da cidade."},
        {"nome": "Recinto do Festival de Inverno", "nota": 4.4, "endereco": "Av. Dr. Luís Arrobas Martins, 1880", "descricao": "Complexo do Auditório e do Museu, palco do Festival de Inverno em julho."},
    ],
    "Cultura": [
        {"nome": "Museu Felícia Leirner", "nota": 4.9, "endereco": "Av. Dr. Luís Arrobas Martins, 1880", "descricao": "Museu ao ar livre com 85 esculturas integradas à paisagem da serra."},
        {"nome": "Auditório Cláudio Santoro", "nota": 4.9, "endereco": "Av. Dr. Luís Arrobas Martins, 1880", "descricao": "Sala de concertos sede do Festival de Inverno, referência arquitetônica."},
        {"nome": "Palácio Boa Vista", "nota": 4.7, "endereco": "Av. Adhemar de Barros, 3001", "descricao": "Residência oficial de inverno do governador, com acervo de arte brasileira."},
        {"nome": "Mosteiro São João (Beneditino)", "nota": 4.8, "endereco": "Av. Dr. Adhemar de Barros, 330", "descricao": "Mosteiro beneditino com igreja, canto gregoriano e produtos dos monges."},
        {"nome": "Casa da Xilogravura", "nota": 4.7, "endereco": "Av. Eduardo Moreira da Cruz, 295 - Jaguaribe", "descricao": "Museu dedicado à xilogravura brasileira, com ateliê e jardim."},
        {"nome": "Igreja Matriz de Santa Teresinha", "nota": 4.5, "endereco": "Praça Prof. Vicente Rizzo - Abernéssia", "descricao": "Principal igreja da cidade, ponto de referência da Vila Abernéssia."},
        {"nome": "Capela de São Pedro", "nota": 4.4, "endereco": "Alto da Boa Vista", "descricao": "Pequena capela histórica em pedra, com vista para o vale."},
        {"nome": "Vila Inglesa", "nota": 4.5, "endereco": "Alto da Vila Inglesa", "descricao": "Conjunto residencial com arquitetura de inspiração britânica dos anos 1920."},
        {"nome": "Boulevard Genève", "nota": 4.6, "endereco": "Rua Djalma Forjaz - Capivari", "descricao": "Galeria comercial com arquitetura europeia, marco visual de Capivari."},
        {"nome": "Estação Ferroviária Emílio Ribas", "nota": 4.4, "endereco": "Abernéssia", "descricao": "Estação histórica da Estrada de Ferro, patrimônio ferroviário da cidade."},
        {"nome": "Espaço Cultural Dr. Além", "nota": 4.3, "endereco": "Av. Frei Orestes Girardi - Abernéssia", "descricao": "Centro de eventos e exposições da prefeitura, com agenda cultural."},
        {"nome": "Museu do Automóvel", "nota": 4.4, "endereco": "Capivari (verifique funcionamento)", "descricao": "Acervo de carros antigos e clássicos; confirme se está aberto na temporada."},
    ],
    "Compras": [
        {"nome": "Lojas da Vila Capivari", "nota": 4.6, "endereco": "Av. Macedo Soares - Capivari", "descricao": "Grife de inverno, malharias, decoração e chocolates no calçadão de Capivari."},
        {"nome": "Boulevard Genève", "nota": 4.6, "endereco": "Rua Djalma Forjaz - Capivari", "descricao": "Galeria com lojas de moda, presentes e cafés em ambiente europeu."},
        {"nome": "Shopping Pátio Capivari", "nota": 4.5, "endereco": "Av. Macedo Soares - Capivari", "descricao": "Shopping a céu aberto com lojas, praça de alimentação e cinema."},
        {"nome": "Cadij Shopping", "nota": 4.5, "endereco": "Rua Djalma Forjaz - Capivari", "descricao": "Galeria tradicional de Capivari com malharias e artigos regionais."},
        {"nome": "Malharia Genève", "nota": 4.5, "endereco": "Rua Djalma Forjaz - Capivari", "descricao": "Uma das malharias clássicas da cidade, tricôs e peças de inverno."},
        {"nome": "Rua das Malhas (Abernéssia)", "nota": 4.4, "endereco": "Av. Frei Orestes Girardi - Abernéssia", "descricao": "Concentração de fábricas e lojas de malha com preço de atacado."},
        {"nome": "Mercado Municipal", "nota": 4.5, "endereco": "Rua Dr. Djalma Forjaz", "descricao": "Produtos regionais, queijos, embutidos, cachaças e artesanato."},
        {"nome": "Feira de Artesanato do Capivari", "nota": 4.4, "endereco": "Praça do Capivari (fins de semana)", "descricao": "Barracas de artesanato, malhas e comidas típicas aos fins de semana."},
        {"nome": "Chocolate Araucária", "nota": 4.7, "endereco": "Av. Macedo Soares - Capivari", "descricao": "Fábrica e loja de chocolates artesanais típicos da cidade."},
        {"nome": "Loja Baden Baden", "nota": 4.5, "endereco": "Rua Djalma Forjaz - Capivari", "descricao": "Loja da cervejaria com rótulos artesanais e kits para presente."},
        {"nome": "Empório Genève", "nota": 4.4, "endereco": "Rua Djalma Forjaz - Capivari", "descricao": "Vinhos, azeites, geleias e produtos gourmet da serra."},
        {"nome": "Spinassi Chocolates", "nota": 4.5, "endereco": "Av. Macedo Soares - Capivari", "descricao": "Chocolate quente artesanal, bombons e doces típicos para levar."},
    ],
    "Aventura": [
        {"nome": "Tarundu", "nota": 4.7, "endereco": "Av. José Antônio Manso, 1515 - Jaguaribe", "descricao": "Parque de lazer com arvorismo, tirolesa, tobogã, pesca e trilha."},
        {"nome": "Prana Aventura Park", "nota": 4.7, "endereco": "Estrada do Pico do Itapeva", "descricao": "Balanços panorâmicos, tirolesa e trilhas com vista para a Mantiqueira."},
        {"nome": "Tirolesa do Parque Capivari", "nota": 4.5, "endereco": "Parque Capivari", "descricao": "Travessia de tirolesa sobre o parque, no centro de Capivari."},
        {"nome": "Arvorismo no Bosque do Silêncio", "nota": 4.5, "endereco": "Av. Sen. Roberto Simonsen, 1724", "descricao": "Circuito de arvorismo entre as árvores da reserva, para vários níveis."},
        {"nome": "Mountain bike no Horto Florestal", "nota": 4.6, "endereco": "Parque Estadual - Horto Florestal", "descricao": "Trilhas de bike de nível variado dentro do parque estadual."},
        {"nome": "Passeio de quadriciclo", "nota": 4.4, "endereco": "Estrada do Pico do Itapeva (operadoras locais)", "descricao": "Roteiros off-road guiados pelas estradas de terra da serra."},
        {"nome": "Paintball", "nota": 4.3, "endereco": "Jaguaribe (operadoras locais)", "descricao": "Arenas de paintball para grupos e famílias, com equipamento incluso."},
        {"nome": "Voo de balão", "nota": 4.6, "endereco": "Base em Campos do Jordão / Vale do Paraíba", "descricao": "Voo panorâmico ao amanhecer sobre a serra; depende das condições do tempo."},
        {"nome": "Cavalgada", "nota": 4.4, "endereco": "Estrada do Horto Florestal (haras locais)", "descricao": "Passeios a cavalo guiados por trilhas e campos da região."},
        {"nome": "Escalada e rapel na Pedra do Baú", "nota": 4.8, "endereco": "São Bento do Sapucaí (região)", "descricao": "Via ferrata e rapel na formação rochosa mais famosa da Mantiqueira."},
        {"nome": "Trilha ao Pico Agudo", "nota": 4.7, "endereco": "São Bento do Sapucaí (região)", "descricao": "Caminhada até um dos melhores pontos de voo livre e nascer do sol."},
        {"nome": "Passeio de 4x4 na Serra", "nota": 4.4, "endereco": "Serra da Mantiqueira (operadoras locais)", "descricao": "Expedições de jipe por estradas rurais, cachoeiras e mirantes."},
    ],
    "Mirantes": [
        {"nome": "Pico do Itapeva", "nota": 4.9, "endereco": "Estrada do Pico do Itapeva - Alto", "descricao": "A 2.030 m, uma das vistas mais altas e amplas da região.", "tags": ["aventura"]},
        {"nome": "Mirante do Morro do Elefante", "nota": 4.7, "endereco": "Alto do Morro do Elefante", "descricao": "Vista clássica do casario e do vale, ao lado da estação do teleférico."},
        {"nome": "Prana Pôr do Sol", "nota": 4.9, "endereco": "Estrada do Pico do Itapeva", "descricao": "Deck e restaurante charmoso voltados para um pôr do sol inesquecível."},
        {"nome": "Vista Chinesa", "nota": 4.7, "endereco": "Estrada do Pico do Itapeva", "descricao": "Mirante à beira da estrada com vista aberta para a Mantiqueira."},
        {"nome": "Mirante Orizonte", "nota": 4.8, "endereco": "Estrada do Pico do Itapeva", "descricao": "Complexo moderno com deck panorâmico, café e loja."},
        {"nome": "Pedra do Baú", "nota": 4.9, "endereco": "São Bento do Sapucaí (região)", "descricao": "Formação rochosa icônica com escadaria e mirantes no topo.", "tags": ["aventura"]},
        {"nome": "Pico Agudo", "nota": 4.8, "endereco": "São Bento do Sapucaí (região)", "descricao": "Rampa de voo livre com vista privilegiada da Pedra do Baú.", "tags": ["aventura"]},
        {"nome": "Ninho da Águia", "nota": 4.5, "endereco": "Estrada do Ninho da Águia - Alto da Boa Vista", "descricao": "Ponto mais alto da área urbana, com mirante sobre toda a cidade."},
        {"nome": "Mirante do Portal", "nota": 4.5, "endereco": "Entrada da cidade", "descricao": "Vista da chegada em Campos do Jordão, junto ao portal monumental."},
        {"nome": "Mirante das Araucárias", "nota": 4.6, "endereco": "Av. Dr. Adhemar de Barros", "descricao": "Deck de observação em meio às araucárias, no caminho do Palácio."},
        {"nome": "Mirante do Alto do Capivari", "nota": 4.5, "endereco": "Alto do Capivari", "descricao": "Vista do casario de Capivari a partir da parte alta do bairro."},
        {"nome": "Mirante do Cristo Redentor", "nota": 4.4, "endereco": "Alto da Boa Vista", "descricao": "Pequeno mirante junto à imagem do Cristo, bom para o fim de tarde."},
    ],
}


def gerar():
    lista = []
    for categoria, itens in atracoes_data.items():
        n = len(itens)
        if n < POR_CATEGORIA_MIN:
            print(f"AVISO: '{categoria}' tem {n} atrações (abaixo do mínimo de {POR_CATEGORIA_MIN}).")
        if n > POR_CATEGORIA_MAX:
            print(f"AVISO: '{categoria}' tem {n} atrações (acima do máximo de {POR_CATEGORIA_MAX}).")

        base_tag = TAG_POR_CATEGORIA[categoria]
        for a in itens:
            tags = list(a.get("tags", []))
            if base_tag not in tags:
                tags.insert(0, base_tag)
            a["tags"] = tags
            a["categoria"] = categoria
            a.setdefault(
                "maps",
                "https://www.google.com/maps/search/?api=1&query="
                + quote_plus(a["nome"] + " Campos do Jordao"),
            )
            lista.append(a)

    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(lista, f, indent=2, ensure_ascii=False)
        f.write("\n")

    total = len(lista)
    print(f"{total} atrações gravadas em {JSON_PATH} ({len(atracoes_data)} categorias).")
    for categoria, itens in atracoes_data.items():
        print(f"  - {categoria}: {len(itens)}")


if __name__ == "__main__":
    gerar()
