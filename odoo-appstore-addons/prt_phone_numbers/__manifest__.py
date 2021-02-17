###################################################################################
# 
#    Copyright (C) 2020 Cetmix OÜ
#
#   Odoo Proprietary License v1.0
# 
#   This software and associated files (the "Software") may only be used (executed,
#   modified, executed after modifications) if you have purchased a valid license
#   from the authors, typically via Odoo Apps, or if you have received a written
#   agreement from the authors of the Software (see the COPYRIGHT file).
# 
#   You may develop Odoo modules that use the Software as a library (typically
#   by depending on it, importing it and using its resources), but without copying
#   any source code or material from the Software. You may distribute those
#   modules under the license of your choice, provided that this license is
#   compatible with the terms of the Odoo Proprietary License (For example:
#   LGPL, MIT, or proprietary licenses similar to this one).
# 
#   It is forbidden to publish, distribute, sublicense, or sell copies of the Software
#   or modified copies of the Software.
# 
#   The above copyright notice and this permission notice must be included in all
#   copies or substantial portions of the Software.
# 
#   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#   IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#   FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#   IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
#   DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
#   ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#   DEALINGS IN THE SOFTWARE.
#
###################################################################################

{
    "name": "Multi Contacts: Several email addresses for partner,"
    " multiple phone numbers and usernames for partners."
    " Export contacts vCard and QRCode",
    "version": "14.0.2.0.0",
    "summary": """Several email addresses, phone numbers and usernames for partner.
     Share contact as vCard and via QRCode""",
    "author": "Ivan Sokolov, Cetmix",
    "category": "Productivity",
    "license": "OPL-1",
    "price": 69.00,
    "currency": "EUR",
    "support": "odooapps@cetmix.com",
    "website": "https://cetmix.com",
    "live_test_url": "https://demo.cetmix.com",
    "depends": ["base", "mail"],
    "images": ["static/description/banner_contacts.png"],
    "data": [
        "security/groups.xml",
        "security/ir.model.access.csv",
        "data/defaults.xml",
        "views/prt_phone.xml",
        "views/res_partner.xml",
        "wizard/vcard.xml",
    ],
    "installable": True,
    "application": True,
    "auto_install": False,
    "post_init_hook": "post_init_hook",
}
