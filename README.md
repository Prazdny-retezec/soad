# soad

Cílem tohoto projektu je vytvořit řešení pro synchronizaci, ukládání a zálohování dat z kamerových a akustických senzorů. 
Projekt se zaměřuje na vývoj systému, který umožní efektivní sběr, zpracování a správu dat z těchto senzorů. Jedná se tedy
o softwarový nástroj, který poběží v laboratorních podmínkách, bude data sbírat, agregovat je, ukládat a zálohovat.


## Technologický stack

Celá struktura systému je zpracována ve třech kontejnerech pomocí [docker-compose](https://docs.docker.com/compose/):

- [Vue.js](https://vuejs.org/) frontend - SPA
- [FastAPI](https://fastapi.tiangolo.com/) backend - REST API s vlastní dokumentací formou OpenAPI a Swagger
- [Postgres](https://www.postgresql.org/) db - ukládání naplánovaných úloh

Další použité technologie:

- [LabVIEW](https://www.ni.com/en/shop/labview.html) - přijímá a zpracovává data z multispektrální kamery (MS). Musí běžet na PC v laboratoři.
  Využívá se protokol GigE Vision a rozhraní **Gigabit Ethernet**
- [Pylon](https://www.baslerweb.com/en/downloads/software/?downloadCategory.values.label.data=pylon) - pro plné fungování RGB kamery (v tomto projektu byla použita verze 8.1.0)
- [Pypylon](https://github.com/basler/pypylon) - ovladání RGB kamery přes **USB 3**
- [APScheduler](https://github.com/agronholm/apscheduler) - plánování úloh (měření)
- [SQLAlchemy](https://www.sqlalchemy.org/) - SQL toolkit a ORM pro Python
- [Pytest](https://docs.pytest.org/en/stable/) - testování BE 
- [Google Drive](https://workspace.google.com/products/drive/) - nahrávání zazipovaných dat (akustická emis a fotky)
- [AlwaysData](https://www.alwaysdata.com/en/) - nasazení
- Webové sockety a [ZEDO](http://dakel.cz/index.php?pg=prod/dev/zedo_en) - akustická emise (AE)

## Dokumentace

- [Programátorská příručka](docs/cz/programmer/tex/out/main.pdf)
- [Uživatelský manuál](docs/cz/user/tex/out/main.pdf)

## Autoři

- **Matěj Cajthaml** - manažer
- **Daniil Astapenko** - analýza, tech-writing
- **Miroslav Filas** - vývoj (BE)
- **Simona Horáčková** - design, vývoj (FE)
- **Petr Chatrný** - technologický leader, vývoj (BE)
- **Dávid Chomo** - vývoj (BE, FE)
- **Otakar Nosek** - analýza, testing
- **Martin Rafaj** - analýza, QA
- **Lucie Suchánková** - design, vývoj (FE)
- **Miroslav Šutera** - zástupce manažera, DevOps
- **David Vlastník** - vývoj (LabVIEW), tech-writing
