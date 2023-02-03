# Recursos da API

Aqui você vai encontrar informações sobre os recursos padrões da API, para um melhor detalhamento de cada rota, utiliza uma das opções abaixo.

- [Post](./post/post.md)
- [Comment](#Comment)
- [Tag](#Tag)

## Autorização

A autenticação é necessária em todas as rotas, tendo apenas como exceção os métodos GET.

Sendo assim, para obter um token é necessário fazer uma requisição para a rota assim como no exemplo.

Exemplo de request:

```bash
curl -X 'POST' \
  'http://url.com/user/token/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'email=useremail.com&password=password'
```

## Respostas

Todas as requisições tem o seu retorno da seguinte forma.

```javascript
{
  "status": integer
  "message": string,
}
```

## Status Code

Segue uma lista com os status presentes na API, junto de seu significado:

| Status Code | Descrição               |
| :---------- | :---------------------- |
| 200         | `OK`                    |
| 201         | `CREATED`               |
| 204         | `NO CONTENT`            |
| 400         | `BAD REQUEST`           |
| 401         | `UNAUTHORIZED`          |
| 404         | `NOT FOUND`             |
| 500         | `INTERNAL SERVER ERROR` |
