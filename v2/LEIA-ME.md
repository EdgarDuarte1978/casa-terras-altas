# Versão 2 (em validação, não oficial)

Proposta de nova organização do guia, contada na ordem da estadia: chegada, a casa, onde comer (com segmentos por perfil, tipo e preço), o que fazer, informações e despedida.
Usa os mesmos dados e fotos da versão oficial (`../restaurantes.json`, `../atracoes.json` e as pastas de fotos).

- Esta pasta existe **somente** na branch `v2-validacao`. A branch `main` (site publicado) não tem esta pasta.
- Para ver: na branch `v2-validacao`, rode `py -3 -m http.server 8000` na pasta do projeto e abra http://localhost:8000/v2/
- Segmentos como Casal, Família, Aceita pet e Ao ar livre ficam "em preparação" até rodar `py -3 scripts/enriquecer_restaurantes.py --gravar` (precisa da chave do Google). Depois disso a página acende os segmentos sozinha.
