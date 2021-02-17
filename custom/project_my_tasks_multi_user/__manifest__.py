# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    "name": "Project - My Tasks with Multi User Module",
    "author": "James Porlante",
    "website": "http://devnizer.com",
    "summary": """
        Modify my task from project_my_tasks""",
    "description": """
        Modify my task from project_my_tasks to make it compatible with Task_to_multi_users
    """,
    "category": "Project",
    "version": "1.0",
    # any module necessary for this one to work correctly
    "depends": ["Task_to_multi_users", "project_my_tasks"],
    # always loaded
    "data": ["views/task_views.xml"],
    # only loaded in demonstration mode
    "demo": [],
    "application": False,
    "license": "OEEL-1",
}
