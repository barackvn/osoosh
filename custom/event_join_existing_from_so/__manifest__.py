{
    "name": "Events - Join Existing Event in SO",
    "summary": "Join an existing event from sales order",
    "description": """
Join an existing event from sales order
=======================================
    """,
    "author": "James Porlante",
    "category": "Custom",
    "website": "https://www.boxed.cz",
    "license": "LGPL-3",
    "version": "1.0",
    "depends": ["event_create_from_so"],
    "data": [
        "wizard/wizard_join_existing_event_views.xml",
        "views/sale_order_views.xml",
        "views/event_views.xml",
    ],
    "installable": True,
}
