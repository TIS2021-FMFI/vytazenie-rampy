transports balíček
==================

Transports balíček obsahuje väčšinu z logiky webovej aplikácie. Stará sa o evidenciu dopráv v databáze, bližšie v popise submodulov.

Submoduly
----------

transports.admin modul
-----------------------

Obsahuje registráciu modelov do administrácie, aby sa dali jednoducho spravovať v administrácii.

.. automodule:: transports.admin
   :members:
   :undoc-members:
   :show-inheritance:

transports.apps modul
----------------------

Obsahuje potrebnú konfiguráciu pre správny beh Djanga. Nie je potrebné upravovať.

.. automodule:: transports.apps
   :members:
   :undoc-members:
   :show-inheritance:

transports.filters modul
-------------------------

Obsahuje definíciu filtrov, ktoré sa používajú v tabuľkovom pohľade aplikácie. Stará sa teda o filtrovanie prepráv podľa zvolených kritérií užívateľom.

.. automodule:: transports.filters
   :members:
   :undoc-members:
   :show-inheritance:

transports.forms modul
-----------------------

Obsahuje formuláre, ktoré používame na tvorbu a úpravu prepráv. Upravuje pôvodné správanie formuláru v Djanga podľa katalógu požiadaviek - podľa práv umožňuje upraviť iba niektoré polia formulára, či stará sa o rýchlejší chod pomocou cacheovania entít, ktoré sa vo formulári používajú.

.. automodule:: transports.forms
   :members:
   :undoc-members:
   :show-inheritance:

transports.models modul
------------------------

Obsahuje definíciu modelov/entít, ktoré v projekte používame. Definuje na nich polia, indexy, či štandardné usporiadanie.

.. automodule:: transports.models
   :members:
   :undoc-members:
   :show-inheritance:

transports.tests modul
-----------------------

Obsahuje unit testy napísané na kontrolu správneho fungovania projektu.

.. automodule:: transports.tests
   :members:
   :undoc-members:
   :show-inheritance:

transports.urls modul
----------------------

Obsahuje routovanie časti projektu špecifickú pre prácu s prepravami. Napojuje adresy na views.

.. automodule:: transports.urls
   :members:
   :undoc-members:
   :show-inheritance:

transports.utils modul
-----------------------

Obsahuje triedu TransportChangeTracker, ktorú používame na trackovanie zmien nad prepravami. Kóduje jednotlivé zmeny do JSON formátu.

.. automodule:: transports.utils
   :members:
   :undoc-members:
   :show-inheritance:

transports.views modul
-----------------------

Obsahuje definované views, ktoré sa zobrazujú na jednotlivých adresách webovej aplikácie. Definuje takisto views, ktoré sa starajú o export údajov z aplikácie.

.. automodule:: transports.views
   :members:
   :undoc-members:
   :show-inheritance: