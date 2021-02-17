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

import base64
import io

from odoo import api, fields, models

QR_ENABLE = True
try:
    import qrcode
except ImportError:
    QR_ENABLE = False
    pass

# Dict for parsing phone labels
PHONE_TYPES = {
    "0": "MAIN",
    "1": "CELL",
    "2": "WORK",
    "3": "EXT",
    "4": "HOME",
    "5": "FAX",
    "6": "OTHER",
    "7": "EMAIL",
    "8": "USERNAME",
}

# Usename tags for extra keys
UNAMES = [["X-SKYPE:", "skype", "scype"]]


#########################
# Contact export wizard #
#########################
class PRTPhoneExport(models.TransientModel):
    _name = "prt.contact.export.wiz"

    name_format = fields.Selection(
        [
            ("0", "First name, Last name, Additional name"),
            ("1", "Last name, First name, Additional name"),
            ("2", "First name, Middle name, Last name"),
            ("3", "Last name, First name, Middle name"),
            ("4", "Last name, Middle name, First name"),
        ],
        string="Name order",
        required=True,
        help="Name order for name parsing",
    )

    vcard_name = fields.Char(string="Name", default="Odoo_contacts.vcf")
    export_picture = fields.Boolean(
        string="Export picture", default=True, help="Export contact's picture"
    )
    format_number = fields.Boolean(
        string="Format numbers",
        default=True,
        help="Save '+123456789' instead of '1(234)56-7 89'",
    )
    qrcode = fields.Binary(string="QR Code", readonly=True)
    qr_installed = fields.Boolean(
        string="qrcode installed", default=QR_ENABLE, readonly=True
    )
    vcard_ids = fields.Many2many(
        string="Attachment",
        comodel_name="ir.attachment",
        relation="vcard_export_ir_attachments_rel",
        column1="wizard_id",
        column2="attachment_id",
        readonly=True,
    )

    # -- Store qrcode to binary field
    def store_qrcode(self):

        # Exit if failed to load lib
        if not QR_ENABLE:
            self.qrcode = False
            return

        for rec in self:
            # Quit if no format is selected
            if not rec.name_format:
                rec.qrcode = False

            # Prepare list of partners
            partner_ids = self._context.get("active_ids", False)

            # Generate QR Code only for single record
            if len(partner_ids) > 1:
                rec.qrcode = False
                return

            qr = qrcode.QRCode(
                version=None,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(self.generate_vcard(partner_ids, False))
            qr.make(fit=True)
            imgByteArr = io.BytesIO()
            img = qr.make_image()
            img.thumbnail((250, 250))
            img.save(imgByteArr, "PNG")

            if partner_ids and len(partner_ids) == 1:
                rec.qrcode = base64.encodebytes(imgByteArr.getvalue())
            else:
                rec.qrcode = False

    # -- Store vcard to binary field
    @api.onchange("name_format", "export_picture", "format_number")
    def store_vcard(self):
        for rec in self:

            # Quit if no format is selected
            if not self.name_format:
                continue

            # Prepare list of partners
            partner_ids = self._context.get("active_ids", False)
            if partner_ids:
                file = self.generate_vcard(partner_ids, self.export_picture)
                if file:
                    # Create new attachments
                    att_id = self.env["ir.attachment"].create(
                        {
                            "name": self.vcard_name,
                            "store_fname": self.vcard_name,
                            "res_model": "prt.contact.export.wiz",
                            "datas": base64.standard_b64encode(
                                bytearray(file, "utf-8")
                            ),
                        }
                    )
                    # Attach it to the record
                    rec.vcard_ids = [(6, False, [att_id.id])]

                    # Update qr code
                    rec.store_qrcode()

    # -- Generate vCard
    def generate_vcard(self, partner_ids, get_image=False):

        # Prepare list of partners
        if not partner_ids:
            return

        # As for now all profiles are parsed with no difference
        partners = self.env["res.partner"].search([("id", "in", partner_ids)])

        if not partners:
            return
        vcard = ""
        url = (
            self.env["ir.config_parameter"].sudo().get_param("web.base.url")
            + "/web#id="
        )
        for partner in partners:
            # Begin vcard
            item_count = 1  # Using 'itemX' in case we cannot use standard key
            vcard += "BEGIN:VCARD\nVERSION:3.0\nX-OdooID:" + str(partner.id) + "\n"

            # Odoo URL
            # Write to vcard
            item_count_str = str(item_count)
            vcard += (
                "item"
                + item_count_str
                + ".URL:"
                + url
                + str(partner.id)
                + "&model=res.partner&view_type=form\n"
            )
            vcard += "item" + item_count_str + ".X-ABLabel:Odoo Partner\n"
            item_count += 1

            # Decomposed name
            name_lines = partner.name.replace(";", "").split(" ")
            i = 0
            first_name = last_name = additional_name = ";"

            # Parse name
            for name_line in name_lines:

                # First line
                if i == 0:
                    if self.name_format in ["0", "2"]:
                        first_name = name_line + ";"
                    else:
                        last_name = name_line + ";"

                # Second line
                elif i == 1:
                    if self.name_format in ["1", "3"]:
                        first_name = name_line + ";"
                    elif self.name_format == "0":
                        last_name = name_line + ";"
                    else:
                        additional_name = name_line + ";"

                # Third line
                elif i == 2:
                    if self.name_format == "4":
                        first_name = name_line + ";"
                    elif self.name_format == "2":
                        last_name = name_line + ";"
                    else:
                        additional_name = name_line + ";"

                # Increment counter
                i += 1

            # Compose name
            if partner.title:
                vcard += (
                    "N:"
                    + last_name
                    + first_name
                    + additional_name
                    + partner.title.name
                    + ";\n"
                )
            else:
                vcard += "N:" + last_name + first_name + additional_name + ";;\n"

            # Full Name
            name = (
                partner.title.name + " " + partner.name
                if partner.title
                else partner.name
            )
            vcard += "FN:" + name + "\n"

            # Address
            address = ";;"

            if partner.street:
                address += partner.street
            if partner.street2 and partner.street:
                address += " " + partner.street2
            elif partner.street2:
                address += partner.street2

            address += ";"

            if partner.city:
                address += partner.city

            address += ";"

            if partner.state_id:
                address += partner.state_id.name

            address += ";"

            if partner.zip:
                address += partner.zip

            address += ";"

            if partner.country_id:
                address += partner.country_id.name

            if len(address) > 2:
                vcard += "ADR;TYPE=WORK:" + address + "\n"

            # Add company & title

            if partner.parent_id and partner.parent_id.company_type != "person":
                vcard += "ORG:" + partner.parent_id.name + "\n"

            if partner.function:
                vcard += "TITLE:" + partner.function + "\n"

            # Image

            if get_image and partner.image_128:
                vcard += (
                    "PHOTO;ENCODING=b;TYPE=JPEG:"
                    + str(partner.image_128, "utf-8")
                    + "\n"
                )

            # URL

            if partner.website:
                vcard += "URL:" + partner.website + "\n"

            # Add note

            if partner.comment:
                comment = ""
                for line in partner.comment.split("\n"):
                    comment += line + r"\n"
                vcard += "NOTE:" + comment + "\n"

            # ===  Add phones ====
            save_email = True  # Used to store multiple emails
            for phone in partner.phone_number_ids:
                # Choose if to save formatted or non formatted number
                phone_number = (
                    "+" + phone.number_searchable
                    if self.format_number
                    else phone.number
                )

                # Check phone type, select key, create label if needed

                # Other phone
                if phone.type == "6":
                    # Create label from note
                    if phone.note:
                        label = phone.note
                    # Or from tags
                    elif phone.tags:
                        if len(phone.tags) == 1:
                            label = phone.tags[0].name
                        else:
                            label = (tag_name + " " for tag_name in phone.tags)
                    # Use default label otherwise
                    else:
                        label = PHONE_TYPES.get("6")

                    # Write to vcard
                    item_count_str = str(item_count)
                    vcard += "item" + item_count_str + ".TEL:" + phone_number + "\n"
                    vcard += "item" + item_count_str + ".X-ABLabel:" + label + "\n"
                    item_count += 1

                # Email
                elif phone.type == "7":
                    # Save first email

                    if save_email:
                        if phone.note and len(phone.note) > 0:
                            vcard += (
                                "EMAIL;TYPE="
                                + phone.note
                                + ":"
                                + phone.number_searchable
                                + "\n"
                            )
                        else:
                            vcard += "EMAIL;TYPE=WORK:" + phone.number_searchable + "\n"
                        save_email = False
                        continue

                    # Save additional emails

                    if phone.note and len(phone.note) > 0:
                        item_count_str = str(item_count)
                        vcard += (
                            "item"
                            + item_count_str
                            + ".EMAIL;TYPE="
                            + phone.note
                            + ":"
                            + phone.number_searchable
                            + "\n"
                        )
                        vcard += (
                            "item" + item_count_str + ".X-ABLabel:" + phone.note + "\n"
                        )
                        item_count += 1

                    else:
                        vcard += "EMAIL;TYPE=WORK:" + phone.number_searchable + "\n"

                # Username
                elif phone.type == "8":
                    # Create separate record for each tag found
                    # If no tags are found use 'note' to store record as URL
                    # Otherwise store as URL with default label
                    if phone.tags:
                        for tag in phone.tags:
                            key = False
                            # Search for pre-defined keys first
                            for uname in UNAMES:
                                if any(
                                    tag.name.replace(" ", "").lower() in s
                                    for s in uname
                                ):
                                    key = uname[0]
                                    break

                            # Create record with pre-defined key if key matches
                            if key:
                                vcard += key + phone.number_searchable + "\n"
                            # Else save as URL
                            else:
                                item_count_str = str(item_count)
                                vcard += (
                                    "item"
                                    + item_count_str
                                    + ".URL:"
                                    + phone.number_searchable
                                    + "\n"
                                )
                                vcard += (
                                    "item"
                                    + item_count_str
                                    + ".X-ABLabel:"
                                    + tag.name
                                    + "\n"
                                )
                                item_count += 1

                    # Try to use note as label
                    elif phone.note:
                        item_count_str = str(item_count)
                        vcard += (
                            "item"
                            + item_count_str
                            + ".URL:"
                            + phone.number_searchable
                            + "\n"
                        )
                        vcard += (
                            "item" + item_count_str + ".X-ABLabel:" + phone.note + "\n"
                        )
                        item_count += 1
                    else:
                        item_count_str = str(item_count)
                        vcard += (
                            "item"
                            + item_count_str
                            + ".URL:"
                            + phone.number_searchable
                            + "\n"
                        )
                        vcard += (
                            "item"
                            + item_count_str
                            + ".X-ABLabel:"
                            + PHONE_TYPES.get("8")
                            + "\n"
                        )
                        item_count += 1

                # Extension
                elif phone.type == "3":
                    item_count_str = str(item_count)
                    vcard += "item" + item_count_str + ".TEL:" + phone_number + "\n"
                    vcard += (
                        "item"
                        + item_count_str
                        + ".X-ABLabel:"
                        + PHONE_TYPES.get("3")
                        + "\n"
                    )
                    item_count += 1

                # Other numbers
                else:
                    vcard += (
                        "TEL;TYPE="
                        + PHONE_TYPES.get(phone.type)
                        + ":"
                        + phone_number
                        + "\n"
                    )

            # END OF VCARD
            vcard += "END:VCARD\n"

        return vcard
