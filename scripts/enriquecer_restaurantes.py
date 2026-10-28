#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Coleta, no Google Places API (New), os ATRIBUTOS de cada restaurante de restaurantes.json
(aceita cachorro, bom para criancas, mesas ao ar livre, reserva, cafe da manha, comida vegetariana...)
e grava em cada item o campo "atributos". Esses dados alimentam os segmentos
"Casal", "Familia com criancas", "Aceita pet", "Ao ar livre", "Grupos", "Cafe da manha" e "Vegetariano".

Uso (na pasta do projeto, com a chave definida no ambiente: set GOOGLE_PLACES_API_KEY=...):
    py -3 scripts/enriquecer_restaurantes.py            -> teste: mostra o resumo, NAO grava
    py -3 scripts/enriquecer_restaurantes.py --gravar   -> grava "atributos" em restaurantes.json

Custo: uma consulta de Place Details por restaurante (campos da faixa Enterprise + Atmosphere).
O Google devolve cada atributo como true/false, ou nao devolve quando nao sabe; este script
NUNCA inventa: atributo ausente fica ausente.
"""
import argparse
import json
import sys
import time
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _places_utils import DETAILS_URL, obter_api_key_validada  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent

# campo do Google -> nome curto gravado no JSON
CAMPOS = {
    "allowsDogs": "aceita_pet",
    "goodForChildren": "bom_para_criancas",
    "menuForChildren": "menu_infantil",
    "goodForGroups": "bom_para_grupos",
    "outdoorSeating": "ao_ar_livre",
    "reservable": "aceita_reserva",
    "liveMusic": "musica_ao_vivo",
    "servesBreakfast": "cafe_da_manha",
    "servesBrunch": "brunch",
    "servesLunch": "almoco",
    "servesDinner": "jantar",
    "servesVegetarianFood": "vegetariano",
    "servesWine": "vinho",
    "servesCocktails": "coquetel",
    "servesBeer": "cerveja",
}
FIELD_MASK = ",".join(CAMPOS.keys())


def extrair(place):
    """Converte a resposta do Google em {nome_curto: bool}, so com o que o Google informou."""
    return {curto: bool(place[campo]) for campo, curto in CAMPOS.items() if campo in place and place[campo] is not None}


def consultar(place_id, api_key):
    headers = {"X-Goog-Api-Key": api_key, "X-Goog-FieldMask": FIELD_MASK}
    resp = requests.get(DETAILS_URL.format(place_id=place_id), headers=headers, timeout=20)
    resp.raise_for_status()
    return resp.json()


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--gravar", action="store_true", help="grava os atributos em restaurantes.json")
    args = ap.parse_args()

    api_key = obter_api_key_validada()
    caminho = ROOT / "restaurantes.json"
    itens = json.loads(caminho.read_text(encoding="utf-8"))

    contagem = {curto: 0 for curto in CAMPOS.values()}
    sem_dado = []
    for i, item in enumerate(itens, 1):
        pid = item.get("place_id")
        if not pid:
            sem_dado.append(item["nome"])
            continue
        try:
            atributos = extrair(consultar(pid, api_key))
        except requests.HTTPError as e:
            print(f"  [{i}/{len(itens)}] {item['nome']}: erro {e.response.status_code}")
            sem_dado.append(item["nome"])
            continue
        item["atributos"] = atributos
        for curto, valor in atributos.items():
            if valor:
                contagem[curto] += 1
        print(f"  [{i}/{len(itens)}] {item['nome']}: {len(atributos)} atributos informados")
        time.sleep(0.1)

    print("\nResumo (quantos restaurantes TEM o atributo = true):")
    for curto, n in sorted(contagem.items(), key=lambda kv: -kv[1]):
        print(f"  {curto:20s} {n:3d} de {len(itens)}")
    if sem_dado:
        print(f"\nSem atributos ({len(sem_dado)}): " + ", ".join(sem_dado))

    if args.gravar:
        caminho.write_text(json.dumps(itens, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print("\nGravado em restaurantes.json. Faca commit e push para publicar.")
    else:
        print("\n(teste - nada gravado. Rode com --gravar para aplicar.)")


if __name__ == "__main__":
    main()
