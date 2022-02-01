api balíček
===========

Balíček `api` definuje REST API endpointy na komunikáciu s javascriptovým kalendárom, ktorý zobrazuje prepravy v danom týždni. Ďalej umožňuje select inputom na frontende vytvárať nové entity asociované s prepravami - prepravcov, dodávateľov a podobne.

Submoduly
----------

api.serializers module
----------------------

Obsahuje serializéry knižnice Django REST Framework, ktoré umožňujú spoľahlivo serializovať modely Djanga do ľubovoľného zaužívaného formátu. V tomto prípade serializujeme modely do JSONu.

.. automodule:: api.serializers
   :members:
   :undoc-members:
   :show-inheritance:

api.urls module
---------------

Obsahuje konfiguráciu routovania nášho REST API.

.. automodule:: api.urls
   :members:
   :undoc-members:
   :show-inheritance:

api.views module
----------------

Obsahuje definíciu jednotlivých endpointov, ktoré obsluhujú kalendár. Toto API umožňuje kalendáru úpravu a čítanie prepráv podľa query parametrov. Ďalej obsahuje views na tvorbu asociácií prepráv - dodávateľov, prepravcov a podobne.

.. automodule:: api.views
   :members:
   :undoc-members:
   :show-inheritance:
