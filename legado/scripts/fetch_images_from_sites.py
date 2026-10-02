"""
Busca e baixa imagens principais (og:image/twitter:image) para cada restaurante.
Uso:
  python scripts/fetch_images_from_sites.py
  python scripts/fetch_images_from_sites.py --use-search

- Prioridade de fontes: `site` -> `instagram` -> (opcional) busca na web via DuckDuckGo.
- Salva em `images/{id}.jpg` e atualiza `restaurantes.json` para usar o caminho local.

Avisos:
- Buscar resultados de sites automaticamente pode falhar para alguns domínios
  (Google Maps é difícil de raspar). Para melhores resultados, prefira fornecer
  `site` ou `instagram` reais no `restaurantes.json`.

"""

import json
import os
import sys
import argparse
from urllib.parse import urljoin, quote_plus

import requests
from bs4 import BeautifulSoup

ROOT = os.path.dirname(os.path.dirname(__file__))
JSON_PATH = os.path.join(ROOT, 'restaurantes.json')
IMAGES_DIR = os.path.join(ROOT, 'images')
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36'}

os.makedirs(IMAGES_DIR, exist_ok=True)


def duckduckgo_search(query):
    url = 'https://duckduckgo.com/html/'
    try:
        res = requests.get(url, params={'q': query}, headers=HEADERS, timeout=15)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, 'html.parser')
        # tentativa de extrair primeiro link de resultado
        link = None
        a = soup.select_one('a.result__a')
        if a and a.get('href'):
            link = a.get('href')
        else:
            # fallback: primeiro <a> dentro de .results
            container = soup.select_one('.results')
            if container:
                a2 = container.find('a', href=True)
                if a2:
                    link = a2['href']
        return link
    except Exception as e:
        print(f'Erro na busca DuckDuckGo: {e}')
        return None


def fetch_page(url):
    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        r.raise_for_status()
        return r.text, r.url
    except Exception as e:
        print(f'Falha ao buscar {url}: {e}')
        return None, None


def extract_image_from_html(html, base_url=None):
    soup = BeautifulSoup(html, 'html.parser')
    # og:image
    meta = soup.find('meta', property='og:image') or soup.find('meta', attrs={'name': 'og:image'})
    if meta and meta.get('content'):
        return urljoin(base_url or '', meta['content'])
    # twitter:image
    meta2 = soup.find('meta', attrs={'name': 'twitter:image'})
    if meta2 and meta2.get('content'):
        return urljoin(base_url or '', meta2['content'])
    # link rel image_src
    link = soup.find('link', rel='image_src')
    if link and link.get('href'):
        return urljoin(base_url or '', link['href'])
    # fallback: primeira imagem grande
    imgs = soup.find_all('img', src=True)
    if imgs:
        for img in imgs:
            src = img['src']
            if src.lower().endswith(('.jpg', '.jpeg', '.png')):
                return urljoin(base_url or '', src)
    return None


def download_image(url, out_path):
    try:
        r = requests.get(url, headers=HEADERS, timeout=20, stream=True)
        r.raise_for_status()
        with open(out_path, 'wb') as fh:
            for chunk in r.iter_content(1024 * 8):
                fh.write(chunk)
        print(f'Imagem salva: {out_path}')
        return True
    except Exception as e:
        print(f'Erro ao baixar imagem {url}: {e}')
        return False


def main(use_search=False):
    if not os.path.exists(JSON_PATH):
        print('Arquivo restaurantes.json não encontrado.')
        sys.exit(1)

    with open(JSON_PATH, encoding='utf-8') as fh:
        data = json.load(fh)

    changed = False

    for rest in data:
        rid = rest.get('id')
        nome = rest.get('nome')
        print('---')
        print(f'[{rid}] {nome}')

        target_img_path = os.path.join('images', f'{rid}.jpg')
        local_full_path = os.path.join(IMAGES_DIR, f'{rid}.jpg')

        # Skip if local image already exists
        if os.path.exists(local_full_path):
            print('Imagem local já existe, pulando.')
            rest['imagem'] = target_img_path
            continue

        candidates = []
        site = (rest.get('site') or '').strip()
        insta = (rest.get('instagram') or '').strip()

        if site:
            candidates.append(site)
        if insta:
            candidates.append(insta)

        if not candidates and use_search:
            query = f"{nome} Campos do Jordão"
            print(f'Buscando na web: {query}')
            found = duckduckgo_search(query)
            if found:
                print(f'Encontrado link: {found}')
                candidates.append(found)

        image_url = None
        for url in candidates:
            print(f'Tentando fonte: {url}')
            html, final_url = fetch_page(url)
            if not html:
                continue
            img = extract_image_from_html(html, base_url=final_url)
            if img:
                print(f'Imagem encontrada: {img}')
                image_url = img
                break

        if image_url:
            ok = download_image(image_url, local_full_path)
            if ok:
                rest['imagem'] = target_img_path
                changed = True
        else:
            print('Nenhuma imagem encontrada para este restaurante.')

    if changed:
        with open(JSON_PATH, 'w', encoding='utf-8') as fh:
            json.dump(data, fh, ensure_ascii=False, indent=2)
            fh.write('\n')
        print('restaurantes.json atualizado com caminhos locais de imagem.')
    else:
        print('Nenhuma atualização no JSON necessária.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--use-search', action='store_true', help='Tentar buscar site via DuckDuckGo quando site/instagram estiverem vazios')
    args = parser.parse_args()
    main(use_search=args.use_search)
