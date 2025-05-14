# Datamint Case Tecnico


# 🎬 API de Locação de Filmes - Case Técnico FilmesTop.com

Este projeto é uma API RESTful desenvolvida em Flask que simula um sistema de locação de filmes, permitindo que usuários possam:
1. Visualizar a lista de filmes disponíveis por gênero;
2. Visualizar todas as informações sobre um determinado filme;
3. Alugar um filme;
4. Avaliar um filme já alugado, registrando a nota;
5. Visualizar todos os filmes já alugados com notas e datas de locação.

---

## Como executar o projeto

### Pré-requisitos

- Docker
- Docker Compose

### Passos

1. Clone o repositório:
git clone https://github.com/seu-usuario/seu-projeto.git
cd seu-projeto

2. SUba os containers
docker-compose up --build

3. Acesse a API em:
http://localhost:5000

4. Conexão Banco postgresql (Dbeaver):
banco de dados: filmes_api
port: 5432
nome de usuário: filmes_user
senha: postgres

### Rodando migracoes (se necessario):
docker-compose exec app flask db upgrade

### Acesso pelo Swagger (recomendado):
http://localhost:5000/apidocs/

### Testes
Execute os testes usando:

docker-compose exec app pytest



## Tecnologias 

- Python 3.11
- Flask
- Flask-Migrate (versionamento do banco)
- Flask-Caching (cache)
- SQLAlchemy 
- PostgreSQL
- Docker e Docker Compose
- Pytest
- Flassger (Swagger)

---

## Funcionalidades obrigatórias

GET    /filmes/genero/<genero_id>       -> Lista filmes por gênero
GET    /filmes/<filme_id>               -> Detalhes de filme
POST   /alugueis/                       -> Alugar filme (requer X-User-Id)
GET    /alugueis/meus-alugueis          -> Listar alugueis do usuário
POST   /meus-alugueis/<aluguel_id>/avaliar -> Avaliar filme alugado

**Usuário autenticado é simulado via header `X-User-Id`.**

---

## Features opcionais implementadas

- Uso de PostgreSQL como banco de dados
- Testes automatizados cobrindo diferentes cenários com Pytest
- Disponibilização via Docker
- Arquitetura com:
  - Application Factory Pattern.
  - Repository Pattern.
  - Factory Pattern.
- Cache  adicionado no endpoint de listar filmes por gênero (`GET /filmes/genero/<genero_id>`) com Timing de 5 minutos.
- Versionamento de banco via Alembic/Flask-Migrate.
- Adição das colunas `nota_final` e `total_avaliacoes` em Filme via migração.
- Atualização automática de `nota_final` e `total_avaliacoes` ao avaliar um filme.



### Observações Gerais

