# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    "name": "Events - Group Attendees",
    "summary": "Attendee templates for a group of events ",
    "description": """
Key Features
============
When user adds to cart a learning product in the frontend, attendee records are created as well depending on qty ordered
    """,
    "author": "4devnet.com",
    "website": "http://4devnet.com",
    "version": "1.0",
    "depends": [
        "base",
        "account",
        "event_sale",
        "hr",
        "event_custom_4devnet",
        "event_join_existing_from_so",
        "event_join_existing_from_task",
        "website_event_cert_shop",
        "website_learning_product",
        "website_event_late_reg",
    ],
    "data": [
        "views/attendee_views.xml",
        "views/event_views.xml",
        "views/invoice_views.xml",
        "views/sale_order_views.xml",
        "views/task_views.xml",
        # "reports/certificate_templates.xml",
        "reports/certificate_templates_1_1.xml",
        "templates/website_templates.xml",
        "wizard/account_invoice_send.xml",
    ],
    "demo": [],
    "application": False,
    "license": "OEEL-1",
}
