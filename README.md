# soad

Cílem tohoto projektu je vytvořit řešení pro synchronizaci, ukládání a zálohování dat z kamerových a akustických senzorů. 
Projekt se zaměřuje na vývoj systému, který umožní efektivní sběr, zpracování a správu dat z těchto senzorů. Jedná se tedy
o softwarový nástroj, který poběží v laboratorních podmínkách, bude data sbírat, agregovat je, ukládat a zálohovat.


## Technologický stack

Celá struktura systému je zpracována ve třech kontejnerech pomocí [Docker Compose](https://docs.docker.com/compose/):

- [Vue.js](https://vuejs.org/) frontend - SPA
- [FastAPI](https://fastapi.tiangolo.com/) backend - REST API
- [LabVIEW](https://www.ni.com/en/shop/labview.html) - pomocí Python skriptu přijímá a zpracovává data z multispektrální kamery (MS).
Využívá se protokol GigE Vision (rozhraní Gigabit Ethernet)

Další použité technologie:

- [Pypylon](https://github.com/basler/pypylon) - ovladání RGB kamery přes USB rozhraní
- [APScheduler](https://github.com/agronholm/apscheduler) - plánování úloh (měření)
- [SQLAlchemy](https://www.sqlalchemy.org/) - SQL toolkit a ORM pro Python
- [Postgres](https://www.postgresql.org/) - ukládání naplánovaných úloh
- [Cypress](https://www.cypress.io/) a [Pytest](https://docs.pytest.org/en/stable/) - testování FE a BE 
- [Google Drive](https://workspace.google.com/products/drive/) - nahrávání zazipovaných dat
- [AlwaysData](https://www.alwaysdata.com/en/) - nasazení
- Webové sockety a [ZEDO](http://dakel.cz/index.php?pg=prod/dev/zedo_en) - akustická emise (AE)

## Dokumentace

- [Programátorská příručka](./docs/cz/programmer.md)
