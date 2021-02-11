{
    "name": "Events Questions",
    "description": "Questions on Events",
    "category": "Website",
    "version": "1.0",
    "author": "Odoo S.A.",
    "depends": ["website_event", "website_event_questions"],
    "data": [
        "event_view.xml",
        "security/ir.model.access.csv",
        "website_event_template.xml",
        "report/report_event_question_view.xml",
    ],
    "demo": [],
    "installable": True,
}
