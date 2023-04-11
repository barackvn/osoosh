from datetime import datetime

from dateutil.relativedelta import relativedelta
from pytz import timezone

from odoo import http, tools
from odoo.http import request


class EventsRSS(http.Controller):
    @http.route(["/events/rss"], type="http", auth="public")
    def events_rss_feed(self, **post):
        limit = post.get("limit", "50")
        dates = post.get("dates", False)

        domain = [("website_published", "=", True)]

        def sdn(date):
            return date.replace(hour=23, minute=59, second=59).strftime(
                tools.DEFAULT_SERVER_DATETIME_FORMAT
            )

        def sd(date):
            return date.strftime(tools.DEFAULT_SERVER_DATETIME_FORMAT)

        def rfc(sd):
            tz = request.env.user.partner_id.tz
            user_tz = timezone(tz or "utc")
            return sd.strftime("%a, %d %b %Y %H:%M:%S %z")

        today = datetime.now()
        if dates:
            if dates == "today":
                domain += [
                    ("date_end", ">", sd(today)),
                    ("date_begin", "<", sdn(today)),
                ]
            elif dates == "week":
                domain += [
                    (
                        "date_end",
                        ">=",
                        sd(today + relativedelta(days=-today.weekday())),
                    ),
                    (
                        "date_begin",
                        "<",
                        sdn(today + relativedelta(days=6 - today.weekday())),
                    ),
                ]
            elif dates == "nextweek":
                domain += [
                    ("date_end", ">=", sd(today.replace(day=1))),
                    (
                        "date_begin",
                        "<",
                        (today.replace(day=1) + relativedelta(months=1)).strftime(
                            "%Y-%m-%d 00:00:00"
                        ),
                    ),
                ]
            elif dates == "month":
                domain += [
                    ("date_end", ">=", sd(today.replace(day=1))),
                    (
                        "date_begin",
                        "<",
                        (today.replace(day=1) + relativedelta(months=1)).strftime(
                            "%Y-%m-%d 00:00:00"
                        ),
                    ),
                ]
            elif dates == "nextmonth":
                domain += [
                    (
                        "date_end",
                        ">=",
                        sd(today.replace(day=1) + relativedelta(months=1)),
                    ),
                    (
                        "date_begin",
                        "<",
                        (today.replace(day=1) + relativedelta(months=2)).strftime(
                            "%Y-%m-%d 00:00:00"
                        ),
                    ),
                ]
            elif dates == "old":
                domain += [("date_end", "<", today.strftime("%Y-%m-%d 00:00:00"))]
            elif dates == "slunicko":
                domain += [
                    ("date_end", ">", sd(today)),
                    ("date_begin", ">", sdn(today)),
                    ("sale_order_origin", "like", "17ZBX00450"),
                ]
        else:
            domain += [("date_end", ">", sd(today)), ("date_begin", "<", sdn(today))]

        param_obj = request.env["ir.config_parameter"]
        base_url = param_obj.sudo().get_param("web.base.url") or ""
        feed = {
            "title": param_obj.sudo().get_param("rss_title"),
            "link": f"{base_url}/events",
            "description": param_obj.sudo().get_param("rss_description"),
            "language": request.env.context["lang"],
            "email": param_obj.sudo().get_param("rss_email"),
        }
        events = request.env["event.event"].search(domain, limit=int(limit))
        if events:
            feed["pub_date"] = rfc(events[-1].write_date)

        data = []
        for e in events:
            data.append(
                {
                    "title": e.name,
                    "description": e.description,
                    "link": f"{base_url}{e.website_url}",
                    "image_url": f"{base_url}/web/image/event.event/{e.id}/event_cover_poster",
                    "category": e.event_type_id.name,
                    "pub_date": rfc(e.date_begin),
                }
            )
        feed["events"] = data
        return request.render(
            "events_rss_feed.events_rss_feed",
            feed,
            headers=[("Content-Type", "application/xml")],
        )
