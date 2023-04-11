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

import logging
import re

from odoo import api, fields, models
from odoo.exceptions import ValidationError
from odoo.osv.expression import get_unaccent_wrapper
from odoo.tools.translate import _

_logger = logging.getLogger(__name__)


# -- Format number to store as searchable
def prep_num(number, num_type):
    if num_type in ["7", "8"]:
        return number.replace(" ", "")
    else:
        return re.sub("[^0-9]", "", number)


# -- Remove duplicates from phone_number_ids
def remove_duplicates(phone_number_ids, env):
    new_phone_number_ids = []

    # Check every entry to find similar entries in already sanitized entries
    for phone_number_entry in phone_number_ids:

        # Proceed only create or update
        if phone_number_entry[0] not in [0, 1]:
            new_phone_number_ids.append(phone_number_entry)
            continue

        has_duplicate = False

        # If we update the number or type only get missing vals
        # by is to do correct computations
        if phone_number_entry[0] == 1:

            # Get type and store it so we can use it for next iterations
            if "type" not in phone_number_entry[2]:
                phone_type = (
                    env["prt.phone"].search([("id", "=", phone_number_entry[1])]).type
                    or False
                )
                phone_number_entry[2].update({"type": phone_type})
            else:
                phone_type = phone_number_entry[2].get("type", False)

            # Get number and store it so we can use it for next iterations
            if "number" not in phone_number_entry[2]:
                phone_number = (
                    env["prt.phone"].search([("id", "=", phone_number_entry[1])]).number
                    or False
                )
                phone_number_entry[2].update({"number": phone_number})

        # Take from vals for new entry
        else:
            phone_type = phone_number_entry[2].get("type", False)

        number_formatted = prep_num(phone_number_entry[2].get("number"), phone_type)
        tags = (
            phone_number_entry[2].get("tags", False)[0][2]
            if phone_number_entry[2].get("tags", False)
            else False
        )
        len_tags = len(tags) if tags else 0
        note = phone_number_entry[2].get("note", False)
        len_note = len(note) if note else 0

        for new_entry in new_phone_number_ids:

            # Proceed only newly create or update
            if new_entry[0] not in [0, 1]:
                continue

            if (
                prep_num(
                    new_entry[2].get("number", False), new_entry[2].get("type", False)
                )
                == number_formatted
            ):
                has_duplicate = True

                # Add tags
                if tags and len_tags > 0:
                    new_tags = tags + new_entry[2].get("tags", False)[0][2] or tags
                    new_entry[2].update({"tags": [[6, 0, new_tags]]})

                # Add note
                if note and len_note > 0:
                    new_note = (
                        f'{note} {new_entry[2].get("note", False)}'
                        if new_entry[2].get("note", False)
                        else note
                    )
                    new_entry[2].update({"note": new_note})
                break

        if not has_duplicate:
            new_phone_number_ids.append(phone_number_entry)
    return new_phone_number_ids


##############
# Phone tags #
##############
class PhoneTag(models.Model):
    _name = "prt.phone.tag"
    _description = "Phone numbers and email tags"

    name = fields.Char(string="Name", required=True, translate=True)
    color = fields.Integer(string="Color index", help="Odoo color index from 0 to 9")


########################
# Phone/Email/Username #
########################
class Phone(models.Model):
    _name = "prt.phone"
    _description = "Phone numbers and email addresses"
    _order = "partner_id, type, sequence"
    _rec_name = "number"

    partner_id = fields.Many2one(
        string="Partner", comodel_name="res.partner", required=False, ondelete="cascade"
    )
    image = fields.Binary(related="partner_id.image_128", readonly=True)
    sequence = fields.Integer(
        string="Priority", default=0, help="Lower value = Higher priority!"
    )
    number = fields.Char(
        string="Value",
        required=True,
        help="Phone number can contain any symbols"
        " but only digits will be used while searching! \n "
        " Should start with country code e.g. +1 100 123-4567 \n"
        " Username can contain letters e.g. 'much_username'"
        " but whitespaces will be skipped while searching usernames",
    )
    number_searchable = fields.Char(
        string="Number or Username",
        compute="_compute_number_searchable",
        store="True",
        help="Value formatted for search",
        index=True,
    )
    type = fields.Selection(
        [
            ("0", "Main phone"),
            ("1", "Mobile phone"),
            ("2", "Work phone"),
            ("3", "Extension phone"),
            ("4", "Home phone"),
            ("5", "Fax"),
            ("6", "Other phone"),
            ("7", "Email"),
            ("8", "Username"),
        ],
        string="Type",
        required=True,
        help="Phone type for number or 'Username'"
        " for username containing letters (e.g. Skype name)",
    )

    note = fields.Char(
        string="Note", help="Put your note or comment here", translate=True
    )
    tags = fields.Many2many(
        string="Tags",
        comodel_name="prt.phone.tag",
        relation="prt_phone_tag_rel",
        column1="phone_id",
        column2="tag_id",
        help="Any tags like 'WhatsApp', 'Telegram' etc",
    )

    """
    Constraint used only when creating from own Form View.
    Only one "Main" phone can exist!
    """

    # -- Python Constraint
    @api.constrains("type")
    def _check_main_count(self):
        for rec in self:
            if rec.partner_id:
                main_count = (
                    self.env["res.partner"]
                    .sudo()
                    .search_count(
                        ["&", ("id", "=", rec.partner_id.id), ("type", "=", "0")]
                    )
                )
                if main_count > 0:
                    raise ValidationError(
                        _('Only one "Main" number per partner can exist!')
                    )

    # -- Set formatted phone number
    @api.depends("number")
    def _compute_number_searchable(self):
        for rec in self:
            if rec.number and len(rec.number) > 0:
                rec.number_searchable = prep_num(rec.number, rec.type)
            else:
                rec.number_searchable = False

    # -- Store existing phone numbers and emails
    @api.model
    def init_data(self):

        # Get list of ids of
        self._cr.execute(
            """ SELECT id, phone, mobile, email FROM res_partner prt
                                        WHERE (SELECT COUNT(id) FROM prt_phone
                                         WHERE prt_phone.partner_id = prt.id) = 0
                                        AND (length(prt.phone)>0
                                         OR length(prt.mobile)>0
                                          OR length(prt.email)>0) """
        )
        # Get existing data
        i = 0
        for res in self._cr.fetchall():
            rec = []
            # Main
            if res[1]:
                rec.append([0, False, {"type": "0", "number": res[1]}])
            # Mobile
            if res[2]:
                rec.append([0, False, {"type": "1", "number": res[2]}])
            # Email
            if res[3]:
                rec.append([0, False, {"type": "7", "number": res[3]}])

            partner = self.env["res.partner"].sudo().browse([res[0]])

            partner.sudo().write({"phone_number_ids": rec})
            i += 1

        _logger.info(
            f"Phone/mobile/email import completed! Total {str(i)} records imported"
        )

    # -- Create
    @api.model
    def create(self, vals):
        """
        Check if same number, email or username already exist for this partner
        Return False instead of creating new record if full duplicate is found.
        If unformatted number differs - update existing numbers
         instead of creating new ones.
        If number type is main, mobilem, work, home
         or other change type not to create a duplicate
         """
        number = vals.get("number", False)
        num_type = vals.get("type", False)
        partner_id = vals.get("partner_id", False)
        sequence = vals.get("sequence", 0)

        # Update duplicates instead of creating new record
        if number and num_type and partner_id:
            search_type = (
                ["0", "1", "2", "4", "6"]
                if num_type in ["0", "1", "2", "4", "6"]
                else [num_type]
            )
            duplicates = self.search(
                [
                    "&",
                    "&",
                    ("partner_id", "=", partner_id),
                    ("type", "in", search_type),
                    ("number_searchable", "=", prep_num(number, num_type)),
                ]
            )

            if len(duplicates) > 0:
                if numbers_update_ids := [
                    duplicate.id
                    for duplicate in duplicates
                    if number != duplicate.number
                ]:
                    self.browse(numbers_update_ids).sudo().write(
                        {"number": number, "type": num_type}
                    )

                # Update all duplicates with note if note exist
                note = vals.get("note", False)
                if note and len(note) > 0:
                    for duplicate in duplicates:
                        duplicate.note = (
                            " ".join([duplicate.note, note]) if duplicate.note else note
                        )

                # If tags added - add them to duplicates
                tags = vals.get("tags", False)

                if tags and len(tags) > 0:
                    add_tags = [[4, tag, False] for tag in tags[0][2]]
                    duplicates.sudo().write({"tags": add_tags})

                # We cannot return False. So we will fool ORM))
                return duplicates[0]

        # If new number is 'Main' change other 'Main' numbers to 'Work'
        if partner_id and num_type == "0":
            if other_main := self.search(
                ["&", ("partner_id", "=", partner_id), ("type", "=", "0")]
            ):
                other_main.sudo().write({"type": "2"})

        # If created from legacy form fields change sequence
        #  of existing records of same type
        #     so newly created record will be set as default.
        if sequence == -100500:
            vals["sequence"] = 0
            if other_same := self.search(
                ["&", ("partner_id", "=", partner_id), ("type", "=", num_type)]
            ):
                other_same.sudo().write({"sequence": 1})

        # Create finally)
        return super(Phone, self).create(vals)

    # -- Write
    def write(self, vals):
        """
        In case type is 'Main' change other 'Main' numbers to 'Work'
        """
        other_main = False
        if vals.get("type", False) == "0":
            other_main = self.search(
                [
                    "&",
                    ("partner_id", "in", self.mapped("partner_id").ids),
                    ("type", "=", "0"),
                ]
            )

        res = super(Phone, self).write(vals)
        if other_main:
            other_main.sudo().write({"type": "2"})
        return res


###############
# Res.Partner #
###############
class Partner(models.Model):
    _inherit = "res.partner"

    # -- Default email address from context
    @api.model
    def _default_email(self):
        if email := self._context.get("default_email", False):
            return [(0, False, {"type": "7", "number": email})]

    phone_number_ids = fields.One2many(
        string="Phones/Emails/Usernames",
        comodel_name="prt.phone",
        inverse_name="partner_id",
        default=_default_email,
    )
    phone = fields.Char(compute="_compute_phone", store=True, inverse="_inverse_dummy")
    mobile = fields.Char(
        compute="_compute_mobile", store=True, inverse="_inverse_dummy"
    )
    email = fields.Char(compute="_compute_email", store=True, inverse="_inverse_dummy")
    phone_searchable = fields.Char(
        string="Phone/Email/Username", related="phone_number_ids.number_searchable"
    )
    phone_number_duplicates = fields.One2many(
        string="Duplicates",
        comodel_name="prt.phone",
        compute="_compute_phone_duplicates",
    )
    phone_number_duplicates_count = fields.Integer(
        string="Number of duplicates", compute="_compute_phone_duplicates_count"
    )

    # -- Tweak search args
    @api.model
    def _tweak_args(self, args):
        """
        When searching for phone, mobile or email substitute them with phone_number_ids
        """
        new_args = []

        for arg in args:

            # Workaround for signs
            if type(arg) == "str":
                new_args.append(arg)
                continue

            # Modify domain
            if arg[0] in ["phone", "mobile", "email"]:

                # Keep original expression if just checking if the value is set
                if arg[2] in [True, False]:
                    new_args.append(arg)
                    continue

                # Replace 'negative' args in search
                arg_straight = arg[1].replace("!", "").replace("not ", "")

                # Search for records with the same value
                domain = [("number_searchable", arg_straight, arg[2])]

                # Add type
                if arg[0] == "phone":
                    domain.append(("type", "in", ["0", "2", "4", "6"]))
                elif arg[1] == "mobile":
                    domain.append(("type", "=", "1"))
                else:
                    domain.append(("type", "=", "7"))

                line_ids = self.env["prt.phone"].search(domain)

                # Keep original domain if nothing found
                if len(line_ids) == 0:
                    new_args.append(arg)
                    continue

                # Create new args
                new_args.append(
                    (
                        "phone_number_ids",
                        "not in" if "!" in arg[1] or "not" in arg[1] else "in",
                        line_ids.ids,
                    )
                )
            else:
                new_args.append(arg)
        return new_args

    # -- Search
    def search(self, args, offset=0, limit=None, order=None, count=False):
        return super(Partner, self).search(
            args=self._tweak_args(args),
            offset=offset,
            limit=limit,
            order=order,
            count=count,
        )

    # -- Name search
    @api.model
    def name_search(self, name, args=None, operator="ilike", limit=100):

        if not name or operator not in ("=", "ilike", "=ilike", "like", "=like"):
            return super(Partner, self).name_search(
                name=name, args=args, operator=operator, limit=limit
            )
        self.check_access_rights("read")

        # Cetmix force search by email
        email = False
        if args:
            for arg in args:
                if arg[0] == "email":
                    email = arg
                    args.remove(email)
                    break
        if email:
            email_args = self._tweak_args([("email", operator, email)])
        else:
            email_args = self._tweak_args([("email", operator, name)])

        where_query = self._where_calc(args)
        self._apply_ir_rules(where_query, "read")
        from_clause, where_clause, where_clause_params = where_query.get_sql()
        from_str = from_clause or "res_partner"
        where_str = where_clause and f" WHERE {where_clause} AND " or " WHERE "

        # Compose email query args
        where_query_email = self.with_context(active_test=False)._where_calc(
            email_args
        )
        (
            from_clause_email,
            where_clause_email,
            where_clause_params_email,
        ) = where_query_email.get_sql()

        # search on the name of the contacts and of its company
        search_name = name
        if operator in ("ilike", "like"):
            search_name = "%%%s%%" % name
        if operator in ("=ilike", "=like"):
            operator = operator[1:]

        unaccent = get_unaccent_wrapper(self.env.cr)

        query = """SELECT res_partner.id
                                     FROM {from_str}
                                  {where} ({display_name} {operator} {percent}
                                       OR {reference} {operator} {percent}
                                       OR {vat} {operator} {percent}
                                       OR {email_addresses})
                                       -- don't panic, trust postgres bitmap
                                 ORDER BY {display_name} {operator} {percent} desc,
                                          {display_name}
                                """.format(
            from_str=from_str,
            where=where_str,
            operator=operator,
            email_addresses=where_clause_email,
            display_name=unaccent("res_partner.display_name"),
            reference=unaccent("res_partner.ref"),
            percent=unaccent("%s"),
            vat=unaccent("res_partner.vat"),
        )

        where_clause_params += [search_name] * 3
        where_clause_params += where_clause_params_email  # partner ids
        where_clause_params.append(search_name)  # The last one for sort
        if limit:
            query += " limit %s"
            where_clause_params.append(limit)
        self.env.cr.execute(query, where_clause_params)
        return (
            self.browse(partner_ids).name_get()
            if (partner_ids := [row[0] for row in self.env.cr.fetchall()])
            else []
        )

    # -- Dummy function
    def _inverse_dummy(self):
        return

    # -- Get duplicates of phone numbers, emails & usernames
    def _compute_phone_duplicates(self):
        for rec in self:
            rec.phone_number_duplicates = self.env["prt.phone"].search(
                [
                    "&",
                    ("partner_id", "!=", rec.id),
                    (
                        "number_searchable",
                        "in",
                        rec.phone_number_ids.mapped("number_searchable"),
                    ),
                ]
            )

    # -- Get count of duplicates of phone numbers, emails & usernames
    @api.depends("phone_number_ids.number")
    def _compute_phone_duplicates_count(self):
        for rec in self:
            rec.phone_number_duplicates_count = len(rec.phone_number_duplicates)

    # -- Get phone number
    @api.depends("phone_number_ids", "phone_number_ids.type", "phone_number_ids.number")
    def _compute_phone(self):
        for rec in self:
            found = False
            for number in rec.phone_number_ids:
                if number.type not in ["1", "3", "7", "8"]:
                    rec.phone = number.number
                    found = True
                    break
            # Fallback
            if not found:
                rec.phone = False

    # -- Get mobile number
    @api.depends(
        "phone_number_ids",
        "phone_number_ids.type",
        "phone_number_ids.sequence",
        "phone_number_ids.number",
    )
    def _compute_mobile(self):
        for rec in self:
            found = False
            for number in rec.phone_number_ids:
                if number.type == "1":
                    rec.mobile = number.number
                    found = True
                    break
            # Fallback
            if not found:
                rec.mobile = False

    # -- Get email
    @api.depends(
        "phone_number_ids",
        "phone_number_ids.type",
        "phone_number_ids.sequence",
        "phone_number_ids.number",
    )
    def _compute_email(self):
        for rec in self:
            found = False
            for number in rec.phone_number_ids:
                if number.type == "7":
                    rec.email = number.number_searchable
                    found = True
                    break
            # Fallback
            if not found:
                rec.email = False

    # -- Create
    @api.model
    def create(self, vals):
        """ Override 'create' in case Partner is created by some legacy method
        Check if phone, mobile or email in vals and modify them.
        Set sequence=-100500 so we can detect that number is created
         from original field (legacy method)
        """
        return super(Partner, self).create(self._sanitize_vals(vals))

    # -- Write
    def write(self, vals):
        """ Override 'write' in case Partner data is written by some legacy method
        Check if phone, mobile or email in vals and modify them.
        Set sequence=-100500 so we can detect that number is created
         from original field (legacy method)
        """

        # Check is writing to new record
        if self._context.get("on_create", False):
            return super(Partner, self).write(vals)

        return super(Partner, self).write(self._sanitize_vals(vals))

    # -- Sanitize phone/email values
    def _sanitize_vals(self, vals):
        """
        Sanitizes phone number values
        :param List vals: list of ORM commands
        (e.g. [(4, id), (0, False, {'name'... )
        :return List: sanitized vals
        """
        # Get vals if any and store them as needed
        phone_number_ids = vals.pop("phone_number_ids", [])

        modify_ids = [
            phone_number[1]
            for phone_number in phone_number_ids
            if phone_number[0] == 1
        ]
        # Add/remove phone
        if "phone" in vals:
            number = vals.pop("phone", False)
            if number and len(number) > 0:
                phone_number_ids.append(
                    [0, False, {"type": "0", "number": number, "sequence": -100500}]
                )
            else:
                # Get numbers to delete and add them to list to delete them on write
                for rec in self:
                    if numbers2del := self.env["prt.phone"].search(
                        [
                            ("partner_id", "=", rec.id),
                            ("type", "=", "0"),
                            ("id", "not in", modify_ids),
                            ("number", "=", rec.phone),
                        ]
                    ):
                        for number2del in numbers2del:
                            phone_number_ids.append((2, number2del.id, False))

        # Add/remove mobile
        if "mobile" in vals:
            number = vals.pop("mobile", False)
            if number and len(number) > 0:
                phone_number_ids.append(
                    [0, False, {"type": "1", "number": number, "sequence": -100500}]
                )
            else:
                # Get numbers to delete and add them to list to delete them on write
                for rec in self:
                    if numbers2del := self.env["prt.phone"].search(
                        [
                            ("partner_id", "=", rec.id),
                            ("type", "=", "1"),
                            ("id", "not in", modify_ids),
                            ("number", "=", rec.mobile),
                        ]
                    ):
                        for number2del in numbers2del:
                            phone_number_ids.append((2, number2del.id, False))

        # Add/remove email
        if "email" in vals:
            number = vals.pop("email", False)
            if number and len(number) > 0:
                phone_number_ids.append(
                    [0, False, {"type": "7", "number": number, "sequence": -100500}]
                )
            else:
                # Get numbers to delete and add them to list to delete them on write
                for rec in self:
                    if numbers2del := self.env["prt.phone"].search(
                        [
                            ("partner_id", "=", rec.id),
                            ("type", "=", "7"),
                            ("id", "not in", modify_ids),
                            ("number", "=", rec.email),
                        ]
                    ):
                        for number2del in numbers2del:
                            phone_number_ids.append((2, number2del.id, False))

        # Sanitize phone number list
        if len(phone_number_ids) > 0:
            vals.update(
                {"phone_number_ids": remove_duplicates(phone_number_ids, self.env)}
            )

        return vals


###############
# Res.Company #
###############
class Company(models.Model):
    _inherit = "res.company"

    phone_number_ids = fields.One2many(
        related="partner_id.phone_number_ids", comodel_name="prt.phone"
    )
    phone_number_duplicates = fields.One2many(
        string="Duplicates",
        comodel_name="prt.phone",
        related="partner_id.phone_number_duplicates",
    )
    phone_number_duplicates_count = fields.Integer(
        string="Number of duplicates",
        related="partner_id.phone_number_duplicates_count",
    )


#############
# Res.Users #
#############
class Users(models.Model):
    _inherit = "res.users"

    # -- Create
    @api.model
    def create(self, vals):
        vals["email"] = vals.get("login", False)
        return super(Users, self).create(vals)

    # -- Write
    def write(self, vals):
        if login := vals.get("login", False):
            vals["email"] = login
        return super(Users, self).write(vals)
