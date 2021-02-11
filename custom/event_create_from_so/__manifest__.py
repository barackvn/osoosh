{
    "name": "Event - Create from SO",
    "summary": "Create events from sales order",
    "description": """
Event - Create from Sales Order
===============================
Automates creating of an event/s from sales order lines
    """,
    "author": "James Porlante",
    "category": "Custom",
    "website": "https://www.boxed.cz",
    "license": "LGPL-3",
    "version": "1.0",
    "depends": ["website_event_late_reg"],
    "data": ["views/event_views.xml", "views/sale_views.xml"],
    "installable": True,
}
