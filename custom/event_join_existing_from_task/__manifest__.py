# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    "name": "Events - Join Existing Event in Task",
    "summary": "Join an existing event from task",
    "description": """
Join an existing event from task
""",
    "author": "Devnizer Web Solutions Inc.",
    "website": "http://devnizer.com",
    "category": "",
    "version": "1.0",
    "depends": ["project_create_event_from_task", "event_join_existing_from_so"],
    # always loaded
    "data": [
        "wizard/wizard_manage_event_from_task_views.xml",
        "views/event_views.xml",
        "views/task_views.xml",
    ],
    "demo": [],
    "application": False,
    "license": "OEEL-1",
    "installable": True,
    "auto_install": False,
}
