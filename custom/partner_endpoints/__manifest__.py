# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    "name": "Partner Endpoints",
    "summary": "Partner Endpoints",
    "description": """
Partner Endpoints
=================================================================================
    """,
    "author": "James Porlante",
    "website": "http://devnizer.com",
    "version": "1.1",
    "depends": [
        "registry_parser_integration",
        "event_join_existing_from_so",
        "project_create_event_from_task",
    ],
    "data": ["views/res_config_settings_views.xml"],
    "demo": [],
    "application": False,
    "license": "OEEL-1",
}
