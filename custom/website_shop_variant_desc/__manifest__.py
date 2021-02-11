# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    "name": "Product Variant Description",
    "version": "1.1",
    "summary": "Product variant description and request quote in website",
    "sequence": 30,
    "description": """
Product Variant Description
===========================
Adds a request for quote button on product in website

Toggles description when user selects a particular product variant in website
    """,
    "category": "Accounting & Finance",
    "depends": ["crm", "website_sale"],
    "data": ["templates/product_templates.xml", "views/product_views.xml"],
    "demo": [],
    "installable": True,
    "application": False,
    "auto_install": False,
}
