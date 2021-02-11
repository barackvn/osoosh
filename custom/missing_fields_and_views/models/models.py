from odoo import api, models, fields


CAPACITY_JOIN_DETAIL = [
    ("dont_have_2", "Nemá prostor - 2 učastníci"),
    ("dont_have_4", "Nemá prostor - 4 učastníci"),
    ("dont_have_6", "Nemá prostor - 6 učastníků"),
    ("10_have_2", "Prostor do 10 - 2 učastníci"),
    ("10_have_4", "Prostor do 10 - 4 učastníci"),
    ("10_have_6", "Prostor do 10 - 6 učastníci"),
    ("15_have_2", "Prostor do 15 - 2 učastníci"),
    ("15_have_4", "Prostor do 15 - 4 učastníci"),
    ("15_have_6", "Prostor do 15 - 6 učastníci"),
    ("20_have_2", "Prostor do 20 - 2 učastníci"),
    ("20_have_4", "Prostor do 20 - 4 učastníci"),
    ("20_have_6", "Prostor do 20 - 6 učastníci"),
]


class Task(models.Model):
    _inherit = "project.task"

    x_date = fields.Date(string="Datum Start")
    x_capacity_join_detail = fields.Selection(
        selection=CAPACITY_JOIN_DETAIL, string="Vlastnosti"
    )
    qty_invoiced = fields.Float(string="Vyfakturovano")
    qty_invoice = fields.Float(string="Zbyva k fakturaci")


class EventEvent(models.Model):
    _inherit = "event.event"

    x_fullfilled = fields.Selection(
        selection=[("free", "volno"), ("full", "plno")], string="Kapacita"
    )
    x_type_open_close = fields.Selection(
        selection=[("open", "Open"), ("closed", "Closed")],
        string="Typ události open or close for foriener atendees",
    )
    x_tag = fields.Selection(
        selection=[
            ("done", "Hotovo"),
            ("missing_doc", "Chybi PL"),
            ("missing_attendee", "Chybi Data ucastniku"),
            ("template", "Sablona"),
            ("new", "Nadcházející"),
        ],
        string="Tags",
        help="Vyplnit stav udalosti",
    )
    # x_tag = fields.Char(string="Tags", help="Vyplnit stav udalosti")
