# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    "name": "Registry Parser Integration",
    "summary": "Registry Parser Integration",
    "description": """
Registry Parser Integration
=================================================================================
    """,
    "author": "James Porlante",
    "website": "http://devnizer.com",
    "version": "1.0",
    "depends": ["base_setup", "base_geolocalize", "partner_company_registry", "sale"],
    "data": [
        "data/cron_data.xml",
        "security/ir.model.access.csv",
        "views/res_config_settings_views.xml",
        "views/res_partner_ico_views.xml",
        "views/res_partner_views.xml",
    ],
    "demo": [],
    "application": False,
    "license": "OEEL-1",
}
