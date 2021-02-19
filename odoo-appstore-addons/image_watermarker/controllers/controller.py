# -*- coding: utf-8 -*-
#################################################################################
#
# Copyright (c) 2018-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>:wink:
# See LICENSE file for full copyright and licensing details.
#################################################################################
from itertools import groupby
import sys
import base64
import codecs
import io
import requests

from PIL import Image
from PIL import ImageEnhance
from PIL import ImageDraw, ImageFont

from odoo import http, tools, SUPERUSER_ID, _
from odoo.http import request
from odoo.tools.safe_eval import safe_eval

from odoo.addons.web.controllers.main import WebClient, Binary
from odoo.addons.website_sale.controllers.main import WebsiteSale

import logging
_logger = logging.getLogger(__name__)


class Binary(Binary):

    def wk_watermark_text(self, model, wk_image, watermarker_id):
        margin_left, margin_top = wk_image.size
        wk_image_mode = wk_image.mode
        position = (watermarker_id.margin_left, watermarker_id.margin_top)
        try:
            fill = safe_eval(watermarker_id.text_fill)
        except Exception as e:
            _logger.info("Exception while==text_fill=%r====" % (e))
            fill = (50, 0, 0, 50)  # (47, 79, 79,160)
        watermark = Image.new("RGBA", wk_image.size, color=(0, 0, 0, 0))

        waterdraw = ImageDraw.ImageDraw(watermark, "RGBA")
        addons_path = http.addons_manifest['web']['addons_path']
        font = '/web/static/src/fonts/lato/Lato-Bol-webfont.ttf'
        font_path = addons_path + font
        txt = watermarker_id.name

        size = max(1, 100)
        fontsize = 1
        img_fraction = watermarker_id.scale
        font_obj = ImageFont.truetype(font_path, 1)
        while font_obj.getsize(txt)[0] < img_fraction * margin_left:
            fontsize += 1
            font_obj = ImageFont.truetype(font_path, fontsize)
        fontsize -= 1
        font_obj = ImageFont.truetype(font_path, fontsize)

        waterdraw.text(position, text=txt, fill=fill, font=font_obj)

        if watermarker_id.positioning == 'vertical':
            angle = 45
            watermark = watermark.rotate(angle, expand=1)
        else:
            pass

        transparent_mode = 'RGBA' if wk_image_mode == 'P' else 'RGB'
        transparent = Image.new(mode=transparent_mode,
                                size=wk_image.size, color=(0, 0, 0, 0))
        transparent.paste(wk_image, (0, 0))
        transparent.paste(watermark, None, watermark)
        return transparent

    def wk_watermark_image(self, model, wk_image, watermarker_id):
        wk_image_mode = wk_image.mode
        width, height = wk_image.size
        ratio = width / height
        image_stream = io.BytesIO(
            codecs.decode(watermarker_id.image, 'base64'))
        watermark = Image.open(image_stream).convert("RGBA")

        if model in ['product.template', 'product.product']:
            watermark_width, watermark_height = watermark.size
            img_fraction = watermarker_id.scale
            new_width = int(width * img_fraction)
            new_height = int(height * img_fraction)
            _logger.info("===%r==%r==" % (new_width, new_height))

            watermark = watermark.resize(
                (new_width, new_height), Image.ANTIALIAS)

        position = (watermarker_id.margin_left, watermarker_id.margin_top)

        if watermarker_id.positioning == 'vertical':
            angle = 45
            watermark = watermark.rotate(angle, expand=1)
            wk_image.paste(watermark, position, watermark)
        else:
            wk_image.paste(im=watermark, box=position, mask=0)
        transparent = Image.new(mode='RGBA', size=(
            width, height), color=(0, 0, 0, 0))
        transparent.paste(wk_image, (0, 0))
        transparent.paste(watermark, position, mask=watermark)
        if wk_image_mode == 'RGB':
            transparent = transparent.convert(wk_image_mode)
        else:
            transparent = transparent.convert('P')
        return transparent
    @http.route(['/web/image',
                 '/web/image/<string:xmlid>',
                 '/web/image/<string:xmlid>/<string:filename>',
                 '/web/image/<string:xmlid>/<int:width>x<int:height>',
                 '/web/image/<string:xmlid>/<int:width>x<int:height>/<string:filename>',
                 '/web/image/<string:model>/<int:id>/<string:field>',
                 '/web/image/<string:model>/<int:id>/<string:field>/<string:filename>',
                 '/web/image/<string:model>/<int:id>/<string:field>/<int:width>x<int:height>',
                 '/web/image/<string:model>/<int:id>/<string:field>/<int:width>x<int:height>/<string:filename>',
                 '/web/image/<int:id>',
                 '/web/image/<int:id>/<string:filename>',
                 '/web/image/<int:id>/<int:width>x<int:height>',
                 '/web/image/<int:id>/<int:width>x<int:height>/<string:filename>',
                 '/web/image/<int:id>-<string:unique>',
                 '/web/image/<int:id>-<string:unique>/<string:filename>',
                 '/web/image/<int:id>-<string:unique>/<int:width>x<int:height>',
                 '/web/image/<int:id>-<string:unique>/<int:width>x<int:height>/<string:filename>'], type='http', auth="public")
    def content_image(self, xmlid=None, model='ir.attachment', id=None, field='datas',
                      filename_field='datas_fname', unique=None, filename=None, mimetype=None,
                      download=None, width=0, height=0, crop=False, access_token=None):
        response = super(Binary, self).content_image(
            xmlid=xmlid, model=model, id=id, field=field,
            filename_field=filename_field, unique=unique, filename=filename, mimetype=mimetype,
            download=download, width=width, height=height, crop=crop, access_token=access_token
        )
        watermarker_id = None
        if (id != None) and (model=='product.template' or model=='product.image') and field in ['image_1920','image_1024','image_512','image_256','image_128']:
            template = model == 'product.template' and request.env[model].browse(int(id)).sudo() or request.env[model].browse(int(id)).sudo().product_tmpl_id.sudo()
            product_variant_ids = len(template) and template.product_variant_ids or 0
            product_variant_ids = product_variant_ids and product_variant_ids.filtered(lambda variant: variant.watermarker_id)
            if len(product_variant_ids):
                watermarker_id = product_variant_ids[0].watermarker_id
            elif template and template.product_variant_id:
                watermarker_id = template.product_variant_id.watermarker_id
        elif model == 'product.product' and field in ['image_1920','image_1024','image_512','image_256','image_128']:
            watermarker_id = request.env[model].browse(int(id)).watermarker_id

        if watermarker_id and len(response.response) and watermarker_id.active :
            base64_source = response.response[0]
            image_stream = io.BytesIO(base64_source)
            image = Image.open(image_stream)
            origin_mode = image.mode
            origin_format = image.format
            if watermarker_id.watermarker_type == 'image':
                image = self.wk_watermark_image(
                    model=model, wk_image=image, watermarker_id=watermarker_id)
            else:
                image = self.wk_watermark_text(
                    model=model, wk_image=image, watermarker_id=watermarker_id)
            output = io.BytesIO()
            image.save(output, format=origin_format)
            image_base64 = output.getvalue()
            response = request.make_response(image_base64, response.headers)
            response.mimetype = Image.MIME[origin_format]
            return response
        return response

# class WatermarkWebsiteSale(WebsiteSale):
    
    #  @http.route('/watermark/last/update/on', type="json", auth="public", website=True, csrf=False)  
    #  def get_watermark_last_update_on(self):
    #     watermarks = request.env['product.watermarker'].sudo().search([('active','=',True)])
    #     update_list = []
    #     for watermark in watermarks:
    #         update_list.append(watermarks.write_date.strftime("%d/%m/%y %H:%M:%S"))
    #     _logger.info("\n[Watermark]: ......update_list.......%r..........",update_list) 
    #     return {
    #         "update_list":update_list,
    #     }   