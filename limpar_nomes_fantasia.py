#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Troca o "nome" de cada item de restaurantes.json/atracoes.json (hoje o texto
completo do anuncio no Google, cheio de palavra-chave de SEO) pelo nome
fantasia - o nome pelo qual o cliente realmente conhece o lugar.

Nao inventa nada: o nome fantasia e sempre um recorte literal do proprio nome
que veio do Google. O nome completo original fica preservado no campo
"nome_google", entao nada se perde - so muda o que aparece no card.

Uso:
    py -3 limpar_nomes_fantasia.py                        -> restaurantes.json, dry-run
    py -3 limpar_nomes_fantasia.py --gravar                -> grava
    py -3 limpar_nomes_fantasia.py --arquivo atracoes.json --gravar
"""
import argparse
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent

# nome completo do Google -> nome fantasia (decidido a mao, um por um)
NOME_FANTASIA = {
    # Fondue
    'Restaurante Casa Suíça "A Casa do Fondue"': "Casa Suíça",
    "Restaurante Krokodillo I": "Krokodillo",
    "Rostie Restaurante Fondue e Pizzaria": "Rostie",
    "Cantina Italiana di Nonna Mimi": "Nonna Mimi",
    "Restaurante La Gália": "La Gália",
    "Restaurante Avestruz": "Avestruz",
    "Matterhorn - Empório e Restaurante": "Matterhorn",

    # Pizzaria
    "Café Terraço Pizzaria Artesanal e Bistrô": "Café Terraço",
    "Arte da Pizza - Grande Hotel Campos do Jordão": "Arte da Pizza",
    "Di Marcelo Cecconi | Levare Pizzaria em Campos do Jordão": "Levare Pizzaria",
    "La Fortezza Restaurante e Pizzaria": "La Fortezza",
    "Maná Restaurante e Pizzaria - Campos do Jordão": "Maná",
    "Artesão Restaurante e Pizzaria": "Artesão",
    "la pizza": "La Pizza",

    # Carnes
    "Restaurante Libertango Parrilla Argentina | Campos do Jordão": "Libertango Parrilla Argentina",
    "Restaurante Cacerola | Carnes Nobres e Cortes Argentinos | Massas Artesanais | Parmegiana | Campos do Jordão": "Cacerola",
    "Restaurante Bonanza Grill": "Bonanza Grill",
    "Na Brasa Restaurante e Choperia": "Na Brasa",
    "Restaurante Krokodillo III": "Krokodillo III",
    "Jardim Plátanos | Gastronomia | Fondue | Restaurante | Campos do Jordão": "Jardim Plátanos",
    "Chico Rei - Gastronomia e Bar": "Chico Rei",

    # Cervejaria
    "Vemaguet 67 Microcervejaria e Choperia": "Vemaguet 67",
    "Iceland Aventura - Bar de Gelo": "Iceland Aventura",
    "Luss Cervejaria & Restaurante - Campos do Jordão": "Luss Cervejaria & Restaurante",

    # Cafés
    "Sans Souci Café e Confeitaria": "Sans Souci",
    "Café No Bosque ®": "Café No Bosque",
    "Dona Belandira Confeitaria & Café em Campos do Jordão": "Dona Belandira Confeitaria & Café",
    "Pepita Café em Campos do Jordão": "Pepita Café",
    "Struderia Café da Elaine Coffee Roasters": "Struderia Café",
    "Myriam Café em Campos do Jordão": "Myriam Café",
    "Um Pé de Café em Campos do Jordão": "Um Pé de Café",
    "Empório Recanto de Minas – Cafeteria em Campos do Jordão": "Empório Recanto de Minas",
    "Restaurante e café Ferraz": "Café Ferraz",

    # Atrações (atracoes.json)
    "Praça do Capivari - Campos do Jordão": "Praça do Capivari",
    "Teleférico do Morro do Elefante - WebCampos": "Teleférico do Morro do Elefante",
    "Mercadinho Piratininga - Campos do Jordão": "Mercadinho Piratininga",
    "CARDE | Arte Design Museu": "CARDE",
    "Dreams House | Campos do Jordão": "Dreams House",
    "Trenó de Montanha - Campos do Jordão": "Trenó de Montanha",
    "Vila capivari": "Vila Capivari",
    "Center Suíço - Flats & Shopping": "Center Suíço",
}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--arquivo", default="restaurantes.json", help="JSON a limpar (default: restaurantes.json)")
    ap.add_argument("--gravar", action="store_true", help="Faz backup e grava o arquivo")
    args = ap.parse_args()

    JSON_PATH = ROOT / args.arquivo
    itens = json.loads(JSON_PATH.read_text(encoding="utf-8"))

    trocados = 0
    for item in itens:
        nome_atual = item["nome"]
        novo = NOME_FANTASIA.get(nome_atual)
        if novo and novo != nome_atual:
            print(f'  "{nome_atual}"\n   -> "{novo}"\n')
            item["nome_google"] = nome_atual
            item["nome"] = novo
            trocados += 1

    print(f"Total de nomes simplificados: {trocados} de {len(itens)}")

    if not args.gravar:
        print("\n(dry-run - nada gravado. Rode com --gravar para aplicar.)")
        return

    backup = ROOT / f"{JSON_PATH.stem}_backup_{datetime.now():%Y%m%d_%H%M%S}.json"
    backup.write_text(JSON_PATH.read_text(encoding="utf-8"), encoding="utf-8")
    print(f"Backup salvo em: {backup}")

    JSON_PATH.write_text(json.dumps(itens, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"{JSON_PATH.name} atualizado.")


if __name__ == "__main__":
    main()
