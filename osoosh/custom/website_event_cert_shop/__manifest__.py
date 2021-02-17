{
    "name": "Events - Birth Date and Title in Reg",
    "summary": "Register with birth date and title in shop",
    "description": """
Register with birth date and title in shop
""",
    "author": "James Porlante",
    "category": "Custom",
    "website": "https://www.boxed.cz",
    "license": "LGPL-3",
    "version": "1.0",
    "depends": ["website_event_late_reg", "event_custom_4devnet"],
    "data": [
        "data/cron_data.xml",
        "views/event_views.xml",
        "templates/website_event_templates.xml",
    ],
    "installable": True,
}
