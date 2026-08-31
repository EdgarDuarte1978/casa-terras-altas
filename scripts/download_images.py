"""
Script simples para baixar imagens a partir de um CSV/JSON com mapeamento id -> url.
Uso:
  python scripts/download_images.py --csv imagens.csv
  python scripts/download_images.py --json imagens.json

CSV esperado (headers): id,url
JSON esperado: [{"id": 1, "url": "https://..."}, ...]

O script salva as imagens em `images/{id}.jpg` (substitui se já existir).
"""

import argparse
import csv
import json
import os
import sys
from urllib.request import urlopen, Request


def download(url, path):
    try:
        req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urlopen(req, timeout=30) as response, open(path, "wb") as out_file:
            out_file.write(response.read())
        print(f"Baixado: {path}")
    except Exception as e:
        print(f"Erro ao baixar {url} -> {e}")


def from_csv(path, out_dir):
    with open(path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            id = row.get('id') or row.get('ID')
            url = row.get('url') or row.get('URL')
            if not id or not url:
                print(f"Linha inválida: {row}")
                continue
            out_path = os.path.join(out_dir, f"{id}.jpg")
            download(url, out_path)


def from_json(path, out_dir):
    with open(path, encoding='utf-8') as f:
        data = json.load(f)
    for item in data:
        id = item.get('id')
        url = item.get('url') or item.get('image')
        if id is None or not url:
            print(f"Entrada inválida: {item}")
            continue
        out_path = os.path.join(out_dir, f"{id}.jpg")
        download(url, out_path)


def main():
    parser = argparse.ArgumentParser(description='Baixa imagens para a pasta images/')
    parser.add_argument('--csv', help='Arquivo CSV com colunas id,url')
    parser.add_argument('--json', help='Arquivo JSON com [{"id":..., "url":...}, ...]')
    parser.add_argument('--out', default='images', help='Pasta de saída (default: images)')
    args = parser.parse_args()

    out_dir = args.out
    os.makedirs(out_dir, exist_ok=True)

    if args.csv:
        from_csv(args.csv, out_dir)
    elif args.json:
        from_json(args.json, out_dir)
    else:
        print('Informe --csv ou --json')
        sys.exit(1)

if __name__ == '__main__':
    main()
