# Programátorská příručka

Tento projekt se dělí na tři hlavní složky: `backend`, `frontend` a `labview`.
Více informací je uvedeno v [README](../../README.md), kde je popsán celý technologický stack.

## Lokální vývoj

### Databáze

Nejprve je nutné sestavit a spustit Postgres databázi. Lze to udělat dvěma způsoby: [lokálně nainstalovat](https://www.postgresql.org/download/) nebo použít Docker.
V obou případech je nutné nastavit proměnné `PGDATA`, `POSTGRES_DB`, `POSTGRES_USER` a `POSTGRES_PASSWORD` (jejich hodnoty jsou v souboru `docker-compose.yml`).

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

Je možné také jít cestou docker-compose:

```bash
# Pozor: udělá build všech služeb z .yml (backend, frontend, database)
docker-compose build
# Spustí jenom databázi
docker-compose up database

# Deaktivuje všechny kontejnery
docker-compose down 
```

Po spuštění výše uvedených příkazů by se měla vytvořit databáze s názvem `soad`, kam se budou ukládat veškerá měření. 
Postgres by měl běžet na portu `5002` a být připraveným k akceptaci dotazů.

### Backend

Po spuštění databáze můžeme připravit backend. Je nutné mít nainstalovaný interpret jazyka [Python](https://www.python.org/downloads/) (verze >=3.11). 
Lze použít i docker-compose, ale po každé změně ve zdrojovém kódu bude potřeba vytvořit nový image backendu.

Zpočatku vytvoříme virtuální prostředí a nainstalujeme závislosti. Na macOS/Linux:
```bash
# soad/backend/
python3 -m venv venv

source venv/bin/activate

python3 -m pip install --upgrade pip

pip3 install -r requirements.txt
```

Na Windows:

```shell
# soad/backend/
# Občas py nefunguje (záleží na instalaci), zkusit python3
py -m venv venv

venv\Scripts\activate

py -m pip install --upgrade pip

pip install -r requirements.txt
```

Poté je nutné spustit `main.py` soubor:

```bash
python3 src/main.py
# Windows
# py src/main.py
```

Po krátké době se spustí FastAPI aplikace na adrese [http://localhost:5001](http://localhost:5001).

## Frontend

TODO
