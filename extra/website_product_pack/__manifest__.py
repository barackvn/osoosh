# -*- coding: utf-8 -*-
#################################################################################
#
#   Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#   See LICENSE file for full copyright and licensing details.
#################################################################################
{
    "name": "Website Product Pack",
    "category": "Website",
    # "license": 'OpenERP AGPL + Private Use',
    "summary": """
         Add Bundle Products in your website for increasing your ecommerce""",
    "description": """

====================
**Help and Support**
====================
.. |icon_features| image:: website_product_pack/static/src/img/icon-features.png
.. |icon_support| image:: website_product_pack/static/src/img/icon-support.png
.. |icon_help| image:: website_product_pack/static/src/img/icon-help.png

|icon_help| `Help <https://webkul.com/ticket/open.php>`_ |icon_support| `Support <https://webkul.com/ticket/open.php>`_ |icon_features| `Request new Feature(s) <https://webkul.com/ticket/open.php>`_
    """,
    "sequence": 1,
    "author": "Webkul Software Pvt. Ltd.",
    "website": "http://www.webkul.com",
    "version": "1.0",
    "depends": ["wk_product_pack", "website_sale"],
    "data": [
        # "data/website_product_pack_data.xml",
        "views/website_product_pack_template.xml",
        "security/ir.model.access.csv",
    ],
    "installable": True,
    "application": True,
    "auto_install": False,
    "price": 30,
    "currency": "EUR",
    "images": ["static/description/Banner.png"],
}
