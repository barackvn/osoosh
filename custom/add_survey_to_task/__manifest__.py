# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    "name": "Add Survey To Task",
    "summary": "Add survey to task",
    "description": """
Add survey to task
""",
    "author": "Devnizer Web Solutions Inc.",
    "website": "http://devnizer.com",
    "category": "",
    "version": "1.0",
    "depends": ["project", "survey"],
    # always loaded
    "data": ["security/ir.model.access.csv", "views/project_views.xml"],
    "demo": [],
    "application": False,
    "license": "OEEL-1",
    "installable": True,
    "auto_install": False,
}
