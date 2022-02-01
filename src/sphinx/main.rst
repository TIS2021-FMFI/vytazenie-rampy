main balíček
============

Balíček `main` je základný balíček celého projektu. Obsahuje konfiguráciu projektu a vstupnú bránu pre prijímanie HTTP requestov od webserveru ako Gunicorn. Takisto obsahuje súbor `.env`, ktorý obsahuje konfiguráciu špecifickú pre runtime - to znamená, že každý užívateľ má túto konfiguráciu inú, keďže na produkcii je nastavená na produkčné nastavenia a každý developer si ju vyplnil inak, podľa svojho pripojenia na databázu.

Submoduly
----------

main.admin modul
-----------------

Obsahuje nadpisy v administrácii projektu. Umožňuje globálne upraviť administráciu oproti pôvodným nastaveniam od Djanga.

.. automodule:: main.admin
   :members:
   :undoc-members:
   :show-inheritance:

main.apps modul
----------------

Modul `apps` obsahuje dáta potrebné pre Django na správny beh. Nie je potrebné upravovať.

.. automodule:: main.apps
   :members:
   :undoc-members:
   :show-inheritance:

main.asgi modul
----------------

Modul obsahuje vstupnú bránu pre asynchrónny webserver, ktorý v tomto prípade nepoužívame.

.. automodule:: main.asgi
   :members:
   :undoc-members:
   :show-inheritance:

main.settings module
--------------------

Modul obsahuje všetku internú konfiguráciu Djanga - napr. pripojenie na databázu, miesto statických súborov, nastavenie logovania a podobne. Všetky nastavenia sú zdokumentované v dokumentácii Djanga.

.. automodule:: main.settings
   :members:
   :undoc-members:
   :show-inheritance:

main.urls module
----------------

Obsahuje základnú konfiguráciu routovania webovej aplikácie. Teda jednotlivé routy posúva do ďalších modulov, kde sa ďalej pripájajú na jednotlivé views.

.. automodule:: main.urls
   :members:
   :undoc-members:
   :show-inheritance:

main.wsgi module
----------------

Vstupná brána pre synchrónny webserver. Tento modul používa Gunicorn na pripojenie s Djangom.

.. automodule:: main.wsgi
   :members:
   :undoc-members:
   :show-inheritance:
