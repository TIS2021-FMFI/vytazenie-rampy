#!/bin/zsh
echo "*********************************"
echo "1. Virtualne prostredie"

if ! [[ -x "$(command -v python3)" && -x "$(command -v python)" ]]; then
    echo 'Chyba: Python nie je nainstalovany.'
    exit 1
fi

VENV="$PWD/venv"
if [ -d "$VENV" ]
then
    echo "Virtualne prostredie je vytvorene."
else
    if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]
    then
        echo "Vytvaram virtualne prostredie."
        python -m venv venv
    else
        echo "Vytvaram virtualne prostredie."
        python3 -m venv venv
    fi
fi

echo "*********************************"
echo "2. Aktivacia virtualneho prostredia"

if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]
then
    source ./venv/Scripts/activate
else
    source ./venv/bin/activate
fi

echo "*********************************"

echo "3. Instalacia potrebnych Python kniznic"

if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]
then
    pip install -r requirements.txt
else
    pip install -r requirements-unix.txt
fi

echo "*********************************"

echo "4. Konfiguracia projektu"

if [ -f "$PWD/src/main/.env" ]
then
    echo "Konfiguracny subor uz je vytvoreny. Preskakujem."
else
    echo "Zadaj meno uzivatela v databaze:"
    read user

    echo "Zadaj heslo uzivatela v databaze:"
    read password

    echo "Zadaj adresu databazoveho servera (bez portu):"
    read hostname

    echo "Zadaj port databazoveho servera:"
    read port

    echo "Zadaj nazov databazy:"
    read db

    touch src/main/.env
    printf "DEBUG=on\nSECRET_KEY=\"django-insecure-stb5=ncj-s6uaywj!8oul#9+6yx5y-*famah3n5ua)t_o^-#w\"\nDATABASE_URL=postgresql://$user:$password@$hostname:$port/$db" > src/main/.env
fi

echo "*********************************"

echo "5. Build frontendu"
if ! [ -x "$(command -v npm)" ]; then
    echo 'Chyba: Node.js nie je nainstalovany.'
    exit 1
fi

npm i
npm run build

echo "*********************************"

echo "6. Aplikovanie migracii backendu"
python src/manage.py makemigrations
python src/manage.py migrate

echo "*********************************"
echo "*Projekt uspesne inicializovany!*"
echo "*********************************"

echo "7. Spustenie vyvojarskeho serveru"
python src/manage.py runserver

