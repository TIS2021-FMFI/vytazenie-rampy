accounts balíček
================

Obsahuje logiku, ktorá sa stará o správne fungovanie používateľov, ich autentifikáciu a autorizáciu na vykonávanie operácií v aplikácii.

Submodules
----------

accounts.admin module
---------------------

Upravuje pôvodné správanie administrácie pre používateľské účty a skupiny podľa potrieb zadávateľa z katalógu požiadaviek.

.. automodule:: accounts.admin
   :members:
   :undoc-members:
   :show-inheritance:

accounts.forms module
---------------------

Upravuje formuláre používané na tvorbu a úpravu používateľov v administrácii podľa potrieb zadávateľa.

.. automodule:: accounts.forms
   :members:
   :undoc-members:
   :show-inheritance:

accounts.models module
----------------------

Obsahuje definíciu vlastného modelu používateľa, ktorý dedí od pôvodného používateľa definovaného vo frameworku Django. Upravuje jeho správanie a definuje dodatočné polia potrebné na správnu funkcionalitu a autorizáciu operácií užívateľa.

.. automodule:: accounts.models
   :members:
   :undoc-members:
   :show-inheritance:

accounts.urls module
--------------------

Definuje adresy na prihlasovanie a odhlasovanie užívateľov do/z aplikácie.

.. automodule:: accounts.urls
   :members:
   :undoc-members:
   :show-inheritance:

accounts.views module
---------------------

Definuje views, ktoré sa starajú o prihlasovanie a odhladovenie užívateľov.

.. automodule:: accounts.views
   :members:
   :undoc-members:
   :show-inheritance:
