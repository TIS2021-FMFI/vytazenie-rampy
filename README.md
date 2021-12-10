# vytazenie-rampy
Študentský projekt TIS 2021

## Potrebný softvér
Na spustenie projektu na lokálnom počítači je potrebný Python 3.7 a vyššie, Node.js verziu 14 a vyššie.

## Inštalácia projektu
0. Najjednoduchšia inštalácia projektu je prostredníctvom priloženého skriptu `install.sh`. Spustením skriptu sa vám nainicializuje celý projekt, prebehne inštalácia knižníc na beh backendu, frontendu, prebehne konfigurácia databázového spojenia a spustia sa databázové migrácie.

1. Najprv je potrebné vytvoriť si virtuálne prostredie pre inštaláciu potrebných knižníc. `python -m venv venv` _(Pre niektoré operačné systémy je potrebné použiť namiesto `python` príkaz `python3`)_

2. Keď je virtuálne prostredie vytvorené, je potrebné ho aktivovať.
    - MacOS/Linux - `source venv/bin/activate`
    - Windows - `venv/Scripts/activate`

3. Teraz je možné si nainštalovať potrebné knižnice. `pip install -r requirements.txt`

4. V priečinku `src/main/` sa nachádza súbor `.env.default`, ktorý obsahuje základnú konfiguráciu pre Django. Duplikujte tento súbor a odstráňte z jeho názvu `.default`. Tak zabezpečíte, že Django načíta správne konfiguračné údaje. Do budúcna tu pribudne viacero vecí ako konfigurácia Postgres databázy, či cacheovacieho enginu. Tento mechanizmus zabezpečuje, že žiadne citlivé údaje sa nedostanú na verejný repozitár.

5. V root priečinku je potrebné nainštalovať si potrebné javascriptové balíčky cez `npm`, odporúčam minimálne Node.js verziu `14`. Príkazom `npm i` sa nainštalujú potrebné balíčky. Následne ich treba vybuildiť cez príkaz `npm run build`.

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
