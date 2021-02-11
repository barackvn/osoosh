.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :alt: License: AGPL-3

==============================================
Automatic partner creation based on CRN number
==============================================

This module allows you to create the partners (companies) based on their CRN number.
Name and address of the partner will automatically be completed via ARES Webservice.



Installation
============

To install this module, you need to:

#. Clone the branch 9.0
#. Add the path to this repository in your configuration (addons-path)
#. Update the module list
#. Search for "Partner Create by CRN" in your addons
#. install the module

Usage
=====

On the partner's form view you will have a button in the header, called
"Get ARES Data", available only on companies (is_company field set to True).
Clicking the button will fetch data, when available, from the ARES Webservice, for most of
the CZ coumpanies.



Credits
=======

Images
------

* Odoo Community Association: `Icon <https://github.com/OCA/maintainer-tools/blob/master/template/module/static/description/icon.svg>`_.

Contributors
------------

* Josef Dostal <jdostal@boxed.cz>

Maintainer
----------

.. image:: https://odoo-community.org/logo.png
   :alt: Odoo Community Association
   :target: https://odoo-community.org

This module is maintained by the OCA.

OCA, or the Odoo Community Association, is a nonprofit organization whose
mission is to support the collaborative development of Odoo features and
promote its widespread use.

To contribute to this module, please visit https://odoo-community.org.
