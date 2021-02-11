from odoo import api, models


class ProjectTask(models.Model):
    _inherit = "project.task"


    def name_get(self):
        result = []
        for record in self:
            name = record.name
            if record.partner_id:
                name = "%s (%s)" % (name, record.partner_id.name)
            result.append((record.id, name))
        return result

    @api.model
    def name_search(self, name, args=None, operator="ilike", limit=100):
        args = args or []
        recs = self.browse()
        if name:
            recs = self.search(
                ["|", ("partner_id.name", operator, name), ("name", operator, name)]
                + args,
                limit=limit,
            )
        return recs.name_get()
