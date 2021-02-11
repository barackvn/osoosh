# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    "name": "Procurement - Place SO Lines",
    "summary": "Place SO Lines in Procurement Orders",
    "description": """
Cron job to fix procurement orders without SO Lines
""",
    "author": "Devnizer Web Solutions Inc.",
    "website": "http://devnizer.com",
    "category": "",
    "version": "1.0",
    "depends": ["sale_timesheet", "purchase"],
    # always loaded
    "data": ["data/cron_data.xml"],
    "demo": [],
    "application": False,
    "license": "OEEL-1",
    "installable": True,
    "auto_install": False,
}
