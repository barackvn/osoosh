# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    "name": "Project - Group Task by Product and ZIP",
    "summary": "Group task by product of related SO line and ZIP",
    "description": """
Group task by product of related SO line and first 2 digits of partner ZIP
""",
    "author": "Devnizer Web Solutions Inc.",
    "website": "http://devnizer.com",
    "category": "",
    "version": "1.0",
    "depends": ["sale_timesheet"],
    # always loaded
    "data": ["data/cron_data.xml", "views/task_views.xml"],
    "demo": [],
    "application": False,
    "license": "OEEL-1",
    "installable": True,
    "auto_install": False,
}
