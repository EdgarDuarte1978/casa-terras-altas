#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Funções compartilhadas pelos geradores gerar_restaurantes_google.py e
gerar_atracoes_google.py. Não é executado sozinho.

Critério de seleção ("padrão de fama/custo-benefício" pedido pelo usuário):
    fama = nota * log10(avaliacoes + 1)
Isso favorece lugares FAMOSOS e bem avaliados (nota alta E muita gente avaliou),
em vez de um 5.0 com 3 avaliações. Como o público é de alto poder aquisitivo,
não penalizamos preço alto - só usamos nota + volume de avaliações.
"""
import math
import sys
import time
import unicodedata

import requests


def obter_api_key_validada():
    """Le GOOGLE_PLACES_API_KEY do ambiente e valida que e' um valor limpo
    (so ASCII, sem espacos/traços "espertos" que copiar-colar as vezes introduz).
    Isso evita o erro 'UnicodeEncodeError: latin-1 codec...' ao montar o header HTTP."""
    import os
    bruta = os.environ.get("GOOGLE_PLACES_API_KEY")
    if not bruta:
        print("ERRO: defina GOOGLE_PLACES_API_KEY antes de rodar.")
        print('No cmd:        set GOOGLE_PLACES_API_KEY=sua_chave_aqui')
        print('No PowerShell: $env:GOOGLE_PLACES_API_KEY = "sua_chave_aqui"')
        sys.exit(1)

    chave = bruta.strip()
    suspeitos = [(i, c, hex(ord(c))) for i, c in enumerate(chave) if ord(c) > 126]
    if suspeitos:
        print("ERRO: a GOOGLE_PLACES_API_KEY tem caractere(s) fora do padrao (provavelmente")
        print("de copiar/colar - um traço \"esperto\" (–) no lugar do hifen (-), ou espaço invisivel).")
        print("Caracteres suspeitos encontrados:")
        for i, c, code in suspeitos:
            print(f"  posicao {i}: {c!r} (codigo {code})")
        print("\nDigite a chave manualmente no terminal (sem copiar/colar) ou copie de novo")
        print("direto da tela 'Chaves e credenciais' do Google Cloud Console.")
        sys.exit(1)

    if chave != bruta:
        print("Aviso: havia espaço(s) sobrando no começo/fim da chave - removido automaticamente.")

    return chave

API_URL = "https://places.googleapis.com/v1/places:searchText"

CAMPOS_DO_JORDAO_LAT = -22.7396
CAMPOS_DO_JORDAO_LNG = -45.5913
CAMPOS_DO_JORDAO_RAIO_M = 12000.0

FIELD_MASK = ",".join([
    "places.id",
    "places.displayName",
    "places.formattedAddress",
    "places.rating",
    "places.userRatingCount",
    "places.googleMapsUri",
    "places.businessStatus",
    "places.priceLevel",
    "places.editorialSummary",
])

PRICE_LEVEL_MAP = {
    "PRICE_LEVEL_INEXPENSIVE": "$",
    "PRICE_LEVEL_MODERATE": "$$",
    "PRICE_LEVEL_EXPENSIVE": "$$$",
    "PRICE_LEVEL_VERY_EXPENSIVE": "$$$$",
}

# tenta primeiro com este piso de avaliações; se a categoria nao atingir a meta,
# relaxa a etapas (nunca inventa dado pra completar, so aceita lugares "menos famosos")
FAIXAS_MIN_AVALIACOES = [100, 50, 20, 5]


def normalizar(texto):
    texto = unicodedata.normalize("NFKD", texto or "").encode("ascii", "ignore").decode()
    return texto.lower().strip()


def fama_score(lugar):
    nota = lugar.get("rating") or 0
    avaliacoes = lugar.get("userRatingCount") or 0
    return nota * math.log10(avaliacoes + 1)


def buscar_texto(query, api_key, tipo=None):
    payload = {
        "textQuery": query,
        "languageCode": "pt-BR",
        "maxResultCount": 20,
        "locationBias": {
            "circle": {
                "center": {"latitude": CAMPOS_DO_JORDAO_LAT, "longitude": CAMPOS_DO_JORDAO_LNG},
                "radius": CAMPOS_DO_JORDAO_RAIO_M,
            }
        },
    }
    if tipo:
        payload["includedType"] = tipo

    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": api_key,
        "X-Goog-FieldMask": FIELD_MASK,
    }
    resp = requests.post(API_URL, headers=headers, json=payload, timeout=20)
    resp.raise_for_status()
    return resp.json().get("places", [])


def buscar_categoria_ampla(query, tipo, api_key):
    """Busca com o tipo (mais preciso) E sem tipo (mais amplo), mescla por place_id.
    Isso evita perder lugares famosos que o Google classifica num tipo diferente
    do esperado (ex.: um café que a API não marca como 'cafe')."""
    vistos = {}
    for t in (tipo, None):
        try:
            lugares = buscar_texto(query, api_key, tipo=t)
        except requests.HTTPError:
            lugares = []
        for l in lugares:
            pid = l.get("id")
            if pid and pid not in vistos:
                vistos[pid] = l
        time.sleep(0.15)
    return list(vistos.values())


def endereco_em_campos_do_jordao(lugar):
    return "campos do jordao" in normalizar(lugar.get("formattedAddress", ""))


def operacional(lugar):
    return lugar.get("businessStatus") == "OPERATIONAL"


def selecionar_top_n(candidatos, n, usados_globalmente):
    """Filtra por cidade+operacional, tenta as faixas de MIN_AVALIACOES em ordem
    (mais exigente primeiro) e devolve os N mais 'famosos' (nota * log(avaliações)).
    Retorna (selecionados, faixa_usada)."""
    base = [
        l for l in candidatos
        if operacional(l) and endereco_em_campos_do_jordao(l) and l.get("id") not in usados_globalmente
    ]
    for piso in FAIXAS_MIN_AVALIACOES:
        elegiveis = [l for l in base if (l.get("userRatingCount") or 0) >= piso]
        if len(elegiveis) >= n:
            elegiveis.sort(key=fama_score, reverse=True)
            return elegiveis[:n], piso
    # nem no piso mais baixo deu a meta - devolve o que tiver (sem inventar)
    base.sort(key=fama_score, reverse=True)
    return base[:n], FAIXAS_MIN_AVALIACOES[-1]


def montar_item_comum(lugar):
    preco = PRICE_LEVEL_MAP.get(lugar.get("priceLevel"), "")
    descricao = (lugar.get("editorialSummary") or {}).get("text", "")
    item = {
        "nome": lugar["displayName"]["text"],
        "nota": lugar.get("rating", ""),
        "avaliacoes": lugar.get("userRatingCount", 0),
        "endereco": lugar.get("formattedAddress", ""),
        "descricao": descricao,
        "maps": lugar.get("googleMapsUri", ""),
        "place_id": lugar.get("id", ""),
    }
    if preco:
        item["preco"] = preco
    return item
