#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Coleta, no Google Places API (New), os ATRIBUTOS de cada lugar de restaurantes.json ou atracoes.json
e grava em cada item o campo "atributos". Esses dados alimentam os segmentos da pagina:
  restaurantes: Casal, Familia com criancas, Aceita pet, Ao ar livre, Grupos, Cafe da manha, Vegetariano
  atracoes:     Familia com criancas, Aceita pet, Acessivel, Com estacionamento, Grupos

Uso (na pasta do projeto, com a chave definida no ambiente: set GOOGLE_PLACES_API_KEY=...):
    py -3 scripts/enriquecer_atributos.py --lista restaurantes            -> teste, NAO grava
    py -3 scripts/enriquecer_atributos.py --lista restaurantes --gravar   -> grava em restaurantes.json
    py -3 scripts/enriquecer_atributos.py --lista atracoes --gravar       -> grava em atracoes.json

Custo: uma consulta de Place Details por lugar (campos da faixa Enterprise + Atmosphere).
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

# campo simples do Google -> nome curto gravado no JSON
CAMPOS_SIMPLES = {
    "restaurantes": {
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
    },
    "atracoes": {
        "allowsDogs": "aceita_pet",
        "goodForChildren": "bom_para_criancas",
        "goodForGroups": "bom_para_grupos",
        "restroom": "banheiro",
    },
}
# campos aninhados (so atracoes): accessibilityOptions e parkingOptions
CAMPOS_ANINHADOS = {
    "restaurantes": [],
    "atracoes": ["accessibilityOptions", "parkingOptions"],
}


def extrair(place, lista="restaurantes"):
    """Converte a resposta do Google em {nome_curto: bool}, so com o que o Google informou."""
    out = {curto: bool(place[campo]) for campo, curto in CAMPOS_SIMPLES[lista].items()
           if campo in place and place[campo] is not None}
    if lista == "atracoes":
        acc = place.get("accessibilityOptions")
        if isinstance(acc, dict) and "wheelchairAccessibleEntrance" in acc:
            out["acessivel"] = bool(acc["wheelchairAccessibleEntrance"])
        park = place.get("parkingOptions")
        if isinstance(park, dict) and park:
            out["estacionamento"] = any(bool(v) for v in park.values())
    return out


def field_mask(lista):
    return ",".join(list(CAMPOS_SIMPLES[lista].keys()) + CAMPOS_ANINHADOS[lista])


def consultar(place_id, api_key, lista):
    headers = {"X-Goog-Api-Key": api_key, "X-Goog-FieldMask": field_mask(lista)}
    resp = requests.get(DETAILS_URL.format(place_id=place_id), headers=headers, timeout=20)
    resp.raise_for_status()
    return resp.json()


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--lista", choices=["restaurantes", "atracoes"], required=True)
    ap.add_argument("--gravar", action="store_true", help="grava os atributos no JSON da lista")
    args = ap.parse_args()

    api_key = obter_api_key_validada()
    caminho = ROOT / f"{args.lista}.json"
    itens = json.loads(caminho.read_text(encoding="utf-8"))

    nomes_curtos = list(CAMPOS_SIMPLES[args.lista].values()) + (["acessivel", "estacionamento"] if args.lista == "atracoes" else [])
    contagem = {curto: 0 for curto in nomes_curtos}
    sem_dado = []
    for i, item in enumerate(itens, 1):
        pid = item.get("place_id")
        if not pid:
            sem_dado.append(item["nome"])
            continue
        try:
            atributos = extrair(consultar(pid, api_key, args.lista), args.lista)
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

    print(f"\nResumo (quantos lugares TEM o atributo = true, de {len(itens)}):")
    for curto, n in sorted(contagem.items(), key=lambda kv: -kv[1]):
        print(f"  {curto:20s} {n:3d}")
    if sem_dado:
        print(f"\nSem atributos ({len(sem_dado)}): " + ", ".join(sem_dado))

    if args.gravar:
        caminho.write_text(json.dumps(itens, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"\nGravado em {caminho.name}. Faca commit e push para publicar.")
    else:
        print("\n(teste - nada gravado. Rode com --gravar para aplicar.)")


if __name__ == "__main__":
    main()
