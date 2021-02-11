{
    "name": "Website Events Late Registration",
    "summary": "Allow late registration in events",
    "description": """
Website Events Late Registration
================================
Allow late registration in events
""",
    "author": "James Porlante",
    "category": "Custom",
    "website": "https://www.boxed.cz",
    "license": "LGPL-3",
    "version": "1.0",
    "depends": ["website_event_sale", "website_event_questions"],
    "data": [
        "data/email_templates.xml",
        "templates/website_event_templates.xml",
        "views/event_views.xml",
    ],
    "installable": True,
}
