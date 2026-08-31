Como usar a pasta `images/`

- Salve imagens reais dos restaurantes na pasta `images/` usando o `id` do restaurante como nome de arquivo.
  Ex: para o restaurante com "id": 1, salve `images/1.jpg`.

- Alternativamente, crie um CSV com colunas `id,url` e rode:

```bash
python scripts/download_images.py --csv imagens.csv
```

- Ou um JSON com objetos `[{"id":1,"url":"https://..."}, ...]` e rode:

```bash
python scripts/download_images.py --json imagens.json
```

- O front-end já usa o valor do campo `imagem` em `restaurantes.json`. Se você preferir que todos apontem para imagens locais, atualize o campo `imagem` para `images/{id}.jpg`.
