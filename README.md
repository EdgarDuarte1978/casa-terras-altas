# Guia Casa Terras Altas

Site estático (guia de hóspedes) da **Casa Terras Altas** — Campos do Jordão.
Reúne restaurantes, atrações e informações da casa para quem se hospeda.

## Páginas

| Arquivo | Conteúdo |
|---|---|
| `index.html` | Guia gastronômico — cards de restaurantes com filtro por tipo de cozinha |
| `o_que_fazer.html` | Atrações de Campos do Jordão com filtro por categoria |
| `sobre_a_casa.html` | Anfitriões, como chegar e lembretes da estadia |

Estilo em `style.css`; lógica em `script.js` (restaurantes) e `script_atracoes.js` (atrações).

## Dados

- `restaurantes.json` — gerado por `gerar_restaurantes.py`
- `atracoes.json` — gerado por `gerar_atracoes.py` (10 a 15 atrações por categoria)

```bash
py -3 gerar_atracoes.py      # regrava atracoes.json a partir da curadoria no script
```

> Endereços e notas das atrações são uma curadoria inicial — confirme endereço,
> horário e funcionamento antes de divulgar.

## Rodar localmente

O site carrega os JSON via `fetch()`, então precisa ser servido por HTTP
(não abra os `.html` com duplo clique):

```bash
py -3 -m http.server 8000
# depois abra http://localhost:8000
```

## Publicar

Site 100% estático. Suba os arquivos (menos o que está no `.gitignore`) em
qualquer host estático — GitHub Pages, Netlify, Vercel, Hostinger. Página
inicial: `index.html`.
