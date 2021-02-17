# -*- coding: utf-8 -*-
#################################################################################
# Author      : Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# Copyright(c): 2015-Present Webkul Software Pvt. Ltd.
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
  "name"                 :  "Image Watermarker",
  "summary"              :  """Provide Watermark image for Odoo Website Image.""",
  "category"             :  "Extra Tools",
  "version"              :  "1.2.2",
  "sequence"             :  1,
  "author"               :  "Webkul Software Pvt. Ltd.",
  "license"              :  "Other proprietary",
  "maintainer"           :  "Prakash Kumar",
  "website"              :  "https://store.webkul.com/Odoo-Image-Watermarker.html",
  "description"          :  """Provide Watermark image for Odoo Website Image.
Product Image Watermarker.
Website Image Watermarker.
Watermark image in Odoo
Odoo Watermark
Image Watermark
Text Watermark
Domain Watermark
Watermark
Watermarked image""",
  "live_test_url"        :  "http://odoodemo.webkul.com/?module=image_watermarker",
  "depends"              :  ['website_sale_management'],
  "data"                 :  [
                             'data/data.xml',
                             'views/image_watermark_view.xml',
                            #  'views/templates.xml',
                             'security/ir.model.access.csv',
                            ],
  "images"               :  ['static/description/Banner.png'],
  "application"          :  True,
  "installable"          :  True,
  "price"                :  59.0,
  "currency"             :  "USD",
  "pre_init_hook"        :  "pre_init_check",
}