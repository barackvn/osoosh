{
    "name": "Create Events From Task",
    "summary": "Integration of project tasks to events management",
    "description": """
Integration of project tasks to events management
    """,
    "author": "James Porlante",
    "category": "Custom",
    "website": "https://www.boxed.cz",
    "license": "LGPL-3",
    "version": "1.0",
    "depends": ["sale_timesheet", "website_event_late_reg", "event_create_from_so"],
    "data": ["views/event_views.xml", "views/task_views.xml"],
    "installable": True,
}
