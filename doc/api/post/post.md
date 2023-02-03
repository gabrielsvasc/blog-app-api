# Post

Rota utilizada para listar, criar, atualizar e deletar postagens.

## post/

> Não precisa de autenticação

Lista todas as publicações de forma resumida.

```plaintext
GET /post/
```

Exemplo de request:

```bash
curl -X 'GET' \
  'http://url.com/post/' \
  -H 'accept: application/json'
```

Exemplo de resposta:

```json
[
  {
    "id": 1,
    "title": "Post 1",
    "desc_post": "Gabriel Vasconcelos",
    "image": "/media/post/a6bc52da-e900-4b51-9c85-7295f65c1334.webp"
  },
  {
    "id": 2,
    "title": "Post 2",
    "desc_post": "Gabriel Vasconcelos",
    "image": "/media/post/e6f452ga-e900-4b51-9c85-7295f65c1334.webp"
  }
]
```

## post/:id

> Não precisa de autenticação

Lista uma postagem específica de forma detalhada.

```http
GET /post/:id
```

| Atributo | Tipo    | Obrigatório | Descrição                                     |
| -------- | ------- | ----------- | --------------------------------------------- |
| `id`     | integer | Sim         | ID atrelado a postagem que deve ser detalhada |

Exemplo de request:

```bash
curl -X 'GET' \
  'http://url.com/post/:id' \
  -H 'accept: application/json'
```

Exemplo de resposta:

```json
[
  {
    "id": 1,
    "title": "Post 1",
    "desc_post": "Gabriel Vasconcelos",
    "image": "/media/post/a6bc52da-e900-4b51-9c85-7295f65c1334.webp",
    "post": "Postagem de Teste"
  }
]
```

## post/publish

> Precisa de autenticação

Cria uma postagem com os dados do Body.

```http
POST /post/publish
```

| Campo       | Tipo          | Obrigatório | Descrição                            |
| ----------- | ------------- | ----------- | ------------------------------------ |
| `title`     | string        | Sim         | Título da postagem                   |
| `desc_post` | string        | Sim         | Descrição resumida da postagem       |
| `image`     | string/binary | Sim         | Imagem utilizada na capa da postagem |
| `post `     | string        | Sim         | Texto com a postagem completa        |

Exemplo de request:

```bash
curl -X 'POST' \
  'http://url.com/post/publish/' \
  -H 'accept: application/json' \
  -H 'Authorization: Token YOURTOKEN' \
  -H 'Content-Type: multipart/form-data' \
  -F 'title=Title' \
  -F 'desc_post=Desc' \
  -F 'image=@image.jpg;type=image/jpeg' \
  -F 'post=Post'
```

Exemplo de Body:

```json
[
  {
    "title": "Post 1",
    "desc_post": "Gabriel Vasconcelos",
    "image": "./image.png",
    "post": "Postagem de Teste"
  }
]
```

Exemplo de resposta:

```json
[
  {
    "id": 1,
    "title": "Post 1",
    "desc_post": "Gabriel Vasconcelos",
    "image": "/media/post/a6bc52da-e900-4b51-9c85-7295f65c1334.webp",
    "post": "Postagem de Teste"
  }
]
```

## post/update/:id

> Precisa de autenticação

Atualiza uma postagem existente com os dados do Body.

```http
PATCH /post/update/:id
```

| Atributo | Tipo    | Obrigatório | Descrição                                     |
| -------- | ------- | ----------- | --------------------------------------------- |
| `id`     | integer | Sim         | ID atrelado a postagem que deve ser detalhada |

| Campo       | Tipo          | Obrigatório | Descrição                            |
| ----------- | ------------- | ----------- | ------------------------------------ |
| `title`     | string        | Não         | Título da postagem                   |
| `desc_post` | string        | Não         | Descrição resumida da postagem       |
| `image`     | string/binary | Não         | Imagem utilizada na capa da postagem |
| `post `     | string        | Não         | Texto com a postagem completa        |

Exemplo de request:

```bash
curl -X 'PATCH' \
  'http://url.com/post/publish/' \
  -H 'accept: application/json' \
  -H 'Authorization: Token YOURTOKEN' \
  -H 'Content-Type: multipart/form-data' \
  -F 'title=Title' \
  -F 'desc_post=Desc' \
  -F 'image=@image.jpg;type=image/jpeg' \
  -F 'post=Post'
```

Exemplo de Body:

```json
[
  {
    "title": "Post 5"
  }
]
```

Exemplo de resposta:

```json
[
  {
    "id": 1,
    "title": "Post 5",
    "desc_post": "Gabriel Vasconcelos",
    "image": "/media/post/a6bc52da-e900-4b51-9c85-7295f65c1334.webp",
    "post": "Postagem de Teste"
  }
]
```

## post/delete/:id

> Precisa de autenticação

Deleta uma postagem existente.

```http
DELETE /post/delete/:id
```

| Atributo | Tipo    | Obrigatório | Descrição                                     |
| -------- | ------- | ----------- | --------------------------------------------- |
| `id`     | integer | Sim         | ID atrelado a postagem que deve ser detalhada |

Exemplo de request:

```bash
curl -X 'DELETE' \
  'http://url.com/post/' \
  -H 'accept: */*' \
  -H 'Authorization: TOKEN YOURTOKEN'
```

Exemplo de resposta:

```json
[
  {
    "id": null,
    "title": "Post 1",
    "desc_post": "Gabriel Vasconcelos",
    "image": null,
    "post": "Postagem de Teste"
  }
]
```
