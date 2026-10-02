"""
Script para tentar extrair preço médio por pessoa a partir dos sites listados em restaurantes.json
Gera um arquivo `restaurantes_with_prices.json` com um campo opcional `preco_medio` quando encontrado.

Uso:
    python scripts/fetch_prices.py --input restaurantes.json --output restaurantes_with_prices.json

Observações:
- Tentativas heurísticas: busca por meta tags, texto com padrões 'R$' e palavras-chave ('preço médio', 'média', 'por pessoa').
- Não sobrescreve o arquivo original por padrão; revise antes de mesclar.
- Requer `requests` e `beautifulsoup4`.
"""

import re
import json
import argparse
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

PRICE_REGEX = re.compile(r"R\$\s?\d{1,3}(?:[.,]\d{2})?")
KEYWORDS = ["preço médio", "preco medio", "valor médio", "valor medio", "por pessoa", "por pessoa", "média por pessoa"]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; PriceScraper/1.0; +https://example.org)"
}


def extract_from_text(text):
    if not text:
        return None
    # busca por padrão de preço
    m = PRICE_REGEX.search(text)
    if m:
        return m.group(0)
    # busca por frases próximas às keywords
    lower = text.lower()
    for kw in KEYWORDS:
        if kw in lower:
            # tentar extrair R$ próximo
            # pega janela de 200 chars
            idx = lower.find(kw)
            start = max(0, idx - 200)
            window = text[start: idx + 200]
            m2 = PRICE_REGEX.search(window)
            if m2:
                return m2.group(0)
    return None


def fetch_url(url, timeout=10):
    try:
        r = requests.get(url, headers=HEADERS, timeout=timeout)
        r.raise_for_status()
        return r.text
    except Exception as e:
        return None


def extract_price_from_site(url):
    html = fetch_url(url)
    if not html:
        return None
    soup = BeautifulSoup(html, "html.parser")
    # tentar meta tags comuns
    meta_props = [
        ('meta', {'property':'og:description'}),
        ('meta', {'name':'description'}),
        ('meta', {'property':'og:locale:alternate'}),
    ]
    for tag, attrs in meta_props:
        t = soup.find(tag, attrs=attrs)
        if t and t.get('content'):
            p = extract_from_text(t.get('content'))
            if p:
                return p
    # buscar texto visível
    texts = ' '.join(soup.stripped_strings)
    p = extract_from_text(texts)
    if p:
        return p
    return None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', default='restaurantes.json')
    parser.add_argument('--output', default='restaurantes_with_prices.json')
    parser.add_argument('--timeout', type=int, default=10)
    parser.add_argument('--write-back', action='store_true', help='Sobrescrever o arquivo de entrada (USE COM CUIDADO)')
    args = parser.parse_args()

    with open(args.input, 'r', encoding='utf-8') as f:
        dados = json.load(f)

    changed = False
    for r in dados:
        if 'preco_medio' in r and r['preco_medio']:
            continue
        link = r.get('site') or r.get('instagram') or r.get('maps')
        if not link:
            continue
        print(f"Buscando preço para: {r.get('nome')} -> {link}")
        price = extract_price_from_site(link)
        if price:
            r['preco_medio'] = price
            print(f"  encontrado: {price}")
            changed = True
        else:
            print("  não encontrado")

    if changed:
        out_path = args.output
        with open(out_path, 'w', encoding='utf-8') as f:
            json.dump(dados, f, ensure_ascii=False, indent=2)
        print(f"Arquivo escrito: {out_path}")
        if args.write_back:
            with open(args.input, 'w', encoding='utf-8') as f:
                json.dump(dados, f, ensure_ascii=False, indent=2)
            print(f"Arquivo original sobrescrito: {args.input}")
    else:
        print("Nenhuma alteração encontrada.")

if __name__ == '__main__':
    main()
