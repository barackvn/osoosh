from odoo.api import SUPERUSER_ID, Environment

from . import models  # noqa
from . import wizard  # noqa


def post_init_hook(cr, registry):
    env = Environment(cr, SUPERUSER_ID, {})
    env["prt.phone"].init_data()
