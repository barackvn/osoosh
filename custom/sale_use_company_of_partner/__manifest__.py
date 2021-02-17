# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    "name": "Sales and Tasks - Use Company of Partner",
    "summary": "Use company of partner",
    "description": """
Use company of partner in creating quotations from CRM and in creating Tasks
""",
    "author": "Devnizer Web Solutions Inc.",
    "website": "http://devnizer.com",
    "category": "",
    "version": "1.0",
    "depends": ["sale_crm", "event", "project"],
    # always loaded
    "data": ["data/cron_data.xml", "views/sale_crm_views.xml"],
    "demo": [],
    "application": False,
    "license": "OEEL-1",
    "installable": True,
    "auto_install": False,
}
