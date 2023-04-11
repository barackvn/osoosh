from odoo import api, models
from odoo.osv.expression import get_unaccent_wrapper


class ResPartner(models.Model):
    _inherit = "res.partner"


    def name_get(self):
        """
        Based on base/models/res/res_partner.py
        """
        res = []
        for partner in self:
            name = partner.name or ""
            if partner.company_name or partner.parent_id:
                if not name and partner.type in ["invoice", "delivery", "other"]:
                    name = dict(self.fields_get(["type"])["type"]["selection"])[
                        partner.type
                    ]
                if not partner.is_company:
                    name = f"{partner.commercial_company_name or partner.parent_id.name}, {name}"
            if self._context.get("show_address_only"):
                name = partner._display_address(without_company=True)
            if self._context.get("show_address"):
                name = name + "\n" + partner._display_address(without_company=True)
            name = name.replace("\n\n", "\n")
            name = name.replace("\n\n", "\n")
            if self._context.get("show_email") and partner.email:
                name = f"{name} <{partner.email}>"
            if self._context.get("html_format"):
                name = name.replace("\n", "<br/>")
            if partner.company_registry:
                name = f"[{partner.company_registry}] {name}"
            res.append((partner.id, name))
        return res

    @api.model
    def name_search(self, name, args=None, operator="ilike", limit=100):
        if args is None:
            args = []
        if name and operator in ("=", "ilike", "=ilike", "like", "=like"):
            self.check_access_rights("read")
            where_query = self._where_calc(args)
            self._apply_ir_rules(where_query, "read")
            from_clause, where_clause, where_clause_params = where_query.get_sql()
            where_str = where_clause and f" WHERE {where_clause} AND " or " WHERE "

            # search on the name of the contacts and of its company
            search_name = name
            if operator in ("ilike", "like"):
                search_name = "%%%s%%" % name
            if operator in ("=ilike", "=like"):
                operator = operator[1:]

            unaccent = get_unaccent_wrapper(self.env.cr)

            query = """SELECT id
              FROM res_partner
              {where} (
                {company_registry} {operator} {percent}
                OR {display_name} {operator} {percent}
                OR {reference} {operator} {percent}
                OR {company_registry} {operator} {percent}
              )
              -- don't panic, trust postgres bitmap
              ORDER BY {display_name} {operator} {percent} desc,
                      {display_name}
            """.format(
                where=where_str,
                operator=operator,
                email=unaccent("email"),
                display_name=unaccent("display_name"),
                reference=unaccent("ref"),
                company_registry=unaccent("company_registry"),
                percent=unaccent("%s"),
            )

            where_clause_params += [search_name] * 5
            if limit:
                query += " limit %s"
                where_clause_params.append(limit)
            self.env.cr.execute(query, where_clause_params)
            if partner_ids := map(lambda x: x[0], self.env.cr.fetchall()):
                return self.browse(partner_ids).name_get()
            else:
                return []
        return super(ResPartner, self).name_search(
            name, args, operator=operator, limit=limit
        )
