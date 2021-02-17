# ©  2016 BOXED, s.r.o.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Automatic partner creation based on CRN number",
    "summary": "Using ARES webservice, name and address information will "
    "be fetched and added to the partner.",
    "version": "9.0.1.0.0",
    "category": "Customer Relationship Management",
    "author": "BOXED, s.r.o., " "Odoo Community Association (OCA)",
    "website": "https://www.boxed.cz",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "external_dependencies": {"python": ["ares_util"]},
    "depends": ["base_vat", "registry_parser_integration"],
    "data": ["views/res_partner_view.xml"],
    "images": ["static/description/customer.png", "static/description/customer1.png"],
    "auto_install": False,
}
