{
    "name": "Events Custom 4devnet",
    "summary": "Event accreditations and certifications",
    "description": """
Key Features
====================
* Manage events certificate issuance and accreditations
* Use emails to automatically send event certificates to invoiced attendees
""",
    "author": "4devnet.com",
    "category": "Custom",
    "website": "http://4devnet.com",
    "license": "LGPL-3",
    "version": "1.0",
    "depends": ["event_sale", "partner_company_registry", "mail"],
    "data": [
        "data/events_data.xml",
        "security/ir.model.access.csv",
        "reports/event_certificate_report.xml",
        # "reports/certificate_report.xml",
        "reports/paperformat.xml",
        "views/event_views.xml",
    ],
    "installable": True,
}
