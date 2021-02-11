# -*- coding: utf-8 -*-
#################################################################################
# Author      : Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# Copyright(c): 2015-Present Webkul Software Pvt. Ltd.
# License URL : https://store.webkul.com/license.html/
# All Rights Reserved.
#
#
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#
# You should have received a copy of the License along with this program.
# If not, see <https://store.webkul.com/license.html/>
#################################################################################

{
    "name": "Website Product Pack Disassemble",
    "author": "Webkul Software Pvt. Ltd.",
    "category": "Sales Management",
    "sequence": 1,
    "license": "Other proprietary",
    "summary": "Provides facility to Disassemble Product Pack from Sale Order",
    "depends": ["website_product_pack"],
    "data": ["views/inherit_product_view.xml", "views/website_pack_template.xml"],
    "application": True,
    "installable": True,
    "auto_install": True,
    # "pre_init_hook"        :  "pre_init_check",
}
