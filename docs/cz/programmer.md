# Programátorská příručka

Tento projekt se dělí na tři hlavní složky: `backend`, `frontend` a `labview`.
Více informací je uvedeno v [README](../../README.md), kde je popsán celý technologický stack.

## Lokální vývoj

### Databáze

Nejprve je nutné sestavit a spustit Postgres databázi. Lze to udělat dvěma způsoby: [lokálně nainstalovat](https://www.postgresql.org/download/) nebo použít Docker.

V případě Dockeru je nutné použít následující příkaz:

```bash
docker run --name soad-db -p 5002:5432
-e PGDATA=/var/lib/postgresql/data/db-files/ 
-e POSTGRES_DB=soad  
-e POSTGRES_USER=api 
-e POSTGRES_PASSWORD=changeit 
-v database_volume:/var/lib/postgresql/data/ postgres:17-alpine

# V případě, že neexistuje volume
docker volume create database_volume
```

Je možné také použít docker-compose:

```bash
# Pozor: udělá build všech služeb z .yml (backend, frontend, database)
docker-compose build
# Spustí jenom databázi
docker-compose up database

# Deaktivuje všechny kontejnery
docker-compose down 
```

[//]: # (TODO: popsat nastavení databáze, tvorba tabulek?)

[//]: # (### Backend)

[//]: # ()
[//]: # (Pro spuštění backendu je nutné mít nainstalovaný Python a všechny závislosti:)

[//]: # ()
[//]: # (```bash)

[//]: # (python3 -m venv venv)

[//]: # (source venv/bin/activate)

[//]: # (pip install -r requirements.txt)

[//]: # ()
[//]: # (```)

[//]: # (## Lokální nasazení )

[//]: # (Pro lokální vývoj je nutné nejprve sestavit a spustit FE &#40;Vue.js&#41;, BE &#40;FastAPI&#41; a databázi. )

[//]: # (K tomu využijeme příkazy Docker Compose:)

[//]: # ()
[//]: # (```bash)

[//]: # (# soad/)

[//]: # ()
[//]: # (# Vytvoří FE, BE a db)

[//]: # (docker-compose build )

[//]: # ()
[//]: # (# Spustí FE, BE a db)

[//]: # (docker-compose up)

[//]: # (```)

[//]: # (FE poběží na [http://localhost:5000]&#40;http://localhost:5000&#41; a BE na [http://localhost:5001]&#40;http://localhost:5001&#41;.)
