# Datamint Case Tecnico


#  API de Locação de Filmes - Case Técnico FilmesTop.com

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
git clone https://github.com/thiagoluisbecker/Datamint-Case-Tecnico.git
cd Datamint-Case-Tecnico


2. Suba os containers
`docker-compose up --build`

3. Acesse a API em:
http://localhost:5000 ou http://localhost:5000/apidocs/ (pelo Swagger)

4. Conexão Banco postgresql (Dbeaver):
- banco de dados: filmes_api
- port: 5432
- nome de usuário: filmes_user
- senha: postgres

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

- GET    /filmes/genero/<genero_id> -> Lista filmes por gênero
- GET    /filmes/<filme_id>               -> Detalhes de filme
- POST   /alugueis/                       -> Alugar filme (requer X-User-Id)
- GET    /alugueis/meus-alugueis          -> Listar alugueis do usuário
- POST   /alugueis/meus-alugueis/avaliar/<aluguel_id> -> Avaliar filme alugado

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
- Adição das colunas `nota_final` e `total_avaliacoes` em Filme via migração (em default=0).
- Atualização automática de `nota_final` e `total_avaliacoes` ao avaliar um filme.



## Modelos de dados

### Filme
**Representa um filme disponível para locação.**

- **Atributos:**
  - `id`
  - `nome`
  - `ano`
  - `sinopse`
  - `diretor`
  - `genero_id` (relacionamento com `Genero`)
  - `nota_final` (média calculada automaticamente após avaliações)
  - `total_avaliacoes` (contador incremental de avaliações)

- **Relacionamentos:**
  - Muitos-para-um com `Genero`
  - Um-para-muitos com `Aluguel`

- **Decisões:**
  - Criado como entidade separada para permitir melhor consistência dos dados
  - Permite filtragem apenas por ID (evitando inconsistências causadas por strings soltas)

---

### Genero
**Representa a categoria do filme (por exemplo, Ação, Comédia).**

- **Atributos:**
  - `id`
  - `nome`

- **Relacionamentos:**
  - Um-para-muitos com `Filme`

- **Decisões:**
  - Entidade separada para garantir integridade e facilitar filtro por ID

---

### Usuario
**Representa o usuário que pode alugar e avaliar filmes.**

- **Atributos:**
  - `id`
  - `nome`
  - `email`
  - `celular`

- **Relacionamentos:**
  - Um-para-muitos com `Aluguel`

- **Decisões:**
  - Usuário “logado” simulado via header `X-User-Id`
  - Permite múltiplos alugueis e avaliações

---

### Aluguel
**Representa uma instância de locação de um filme por um usuário.**

- **Atributos:**
  - `id`
  - `usuario_id`
  - `filme_id`
  - `data_locacao`
  - `nota` (opcional, podendo ser preenchida posteriormente)

- **Relacionamentos:**
  - Muitos-para-um com `Usuario`
  - Muitos-para-um com `Filme`

- **Decisões:**
  - Cada aluguel é único e vinculado a um usuário e a um filme
  - Avaliação só pode ser feita se o usuário alugou o filme
  - Cada aluguel só recebe uma única avaliação
