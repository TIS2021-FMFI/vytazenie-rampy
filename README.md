# vytazenie-rampy
Študentský projekt TIS 2021

## Potrebný softvér
Na spustenie projektu na lokálnom počítači je potrebný Python 3.7 a vyššie, Node.js verziu 14 a vyššie.

## Inštalácia projektu
0. Najjednoduchšia inštalácia projektu je prostredníctvom priloženého skriptu `install.sh`. Spustením skriptu sa vám nainicializuje celý projekt, prebehne inštalácia knižníc na beh backendu, frontendu, prebehne konfigurácia databázového spojenia a spustia sa databázové migrácie.

1. Pre import základnej konfigurácie, bez ktorej nie je možné správne fungovanie aplikácie napíšte z koreňového adresára do príkazového riadka `python src/manage.py loaddata import/*`.
Ak ste na Windowse, tak spustite príkazy v nasledovnom poradí.
```
python src/manage.py loaddata import/views.json
python src/manage.py loaddata import/permissions.json
python src/manage.py loaddata import/groups.json
python src/manage.py loaddata import/custom_groups.json
```

2. Na vytvorenie administrátorského účtu spustite `python src/manage.py createsuperuser`.

## Spustenie vývojárskeho serveru
Django prichádza defaultne s vlastným serverom určeným na vývoj na lokálnom počítači. Tento server je možné zapnúť príkazom `python manage.py runserver`. Je potrebné byť v priečinku `./src`, kde sa nachádza súbor `manage.py`.

Server automaticky sleduje zmeny v zdrojovom kóde systému a pri zmene sa automaticky reštartuje. Preto je potrebné ho iba spustiť a zmeny je možné vykonávať bez akéhokoľvek zásahu do behu servera.

## Jednoduchý návod na ovládanie manage.py
- `python manage.py makemigrations` - Ak vykonáte zmenu v definovaných modeloch _(pridáte nové, upravíte existujúce)_, je potrebné aby Django vytvorilo migrácie, ktoré potom musíte zmigrovať do databázy.
- `python manage.py migrate` - Zmigrovanie zmien v databázovej štruktúre. Toto je potrebné urobiť vždy, keď vaša databáza neobsahuje aktuálny stav, ktorý popisujú definované modely v projekte.
- `python manage.py createsuperuser` - Vytvorenie nového administrátora.
- `python manage.py startapp` - Vytvorenie novej "aplikácie" - Django delí logické celky systému na tzv. aplikácie.
- `python manage.py` - Vypísanie existujúcich príkazov pre manage.py.

## Zásady pri tvorení kódu
Codebase chceme udržiavať čistú a čitateľnú. Logickú čistotu musíme zabezpečiť my, ľudia, avšak na formátovanie kódu existujú nástroje oveľa efektívnejšie ako my. Preto už pri inštalovaní knižníc je medzi nimi aj populárny automatický formátovač kódu pre Python - **Black**. Pred pushovaním do repozitára prosím vždy sformátujme kód, nech je ľahko čitateľný už na pull requeste.

Formátovanie je jednoduché, stačí v `./src` zavolať príkaz `black .`.
