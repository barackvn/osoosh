import xmlrpc.client


#v14
url_v_14 = 'http://odoov12ent.boxed.cz'
db_v_14 = 'boxed'
username_v_14 = 'admin@boxed.cz'
password_v_14 = '1Juzepe1'
port_v_14 = '8069'
common_v_14 = xmlrpc.client.ServerProxy('{}:{}/xmlrpc/2/common'.format(url_v_14, port_v_14))
uid_v_14 = common_v_14.authenticate(db_v_14, username_v_14, password_v_14, {})
models_v_14 = xmlrpc.client.ServerProxy('{}:{}/xmlrpc/2/object'.format(url_v_14, port_v_14))
print(uid_v_14)

#v9
url_v_9 = 'https://portal.boxed.cz'
db_v_9 = 'boxed'
username_v_9 = 'admin@boxed.cz'
password_v_9 = '1Juzepe1'
port_v_9 = '443'
common_v_9 = xmlrpc.client.ServerProxy('{}:{}/xmlrpc/2/common'.format(url_v_9, port_v_9))
uid_v_9 = common_v_9.authenticate(db_v_9, username_v_9, password_v_9, {})
models_v_9 = xmlrpc.client.ServerProxy('{}:{}/xmlrpc/2/object'.format(url_v_9, port_v_9))
print(uid_v_9)

done = 1+3+1+53
size = 1000 - done
offset = 0 + done
print('Offset:', offset)
templates = models_v_9.execute_kw(db_v_9, uid_v_9, password_v_9,
    'product.template', 'search_read',[[]],{'offset': offset, 'limit': size})

for i, template in enumerate(templates):
    i = i+1
    print("Processing [%s] %s of %s [%s] %s"%(template['id'], i, size, 100 * i/size, '%'))

    # del template['image_small']
    # del template['image']
    # del template['image_medium']
    template['image_512'] = template['image_small']
    template['image_1920'] = template['image']
    template['image_1024'] = template['image_medium']
    template['currency_id'] = 9
    if template['categ_id']:
        template['categ_id'] = template['categ_id'][0]
    
    if template['uom_id']:
        template['uom_id'] = template['uom_id'][0]
    
    if template['uom_po_id']:
        template['uom_po_id'] = template['uom_po_id'][0]
    
    if template['public_categ_ids']:
        public_categs = models_v_9.execute_kw(db_v_9, uid_v_9, password_v_9,
    'product.public.category', 'search_read',[[('id','in',template['public_categ_ids'])]],{'offset': 0, 'limit': size})
        template['public_categ_ids'] = list()
        for categ in public_categs:
            public_categs = models_v_14.execute_kw(db_v_14, uid_v_14, password_v_14,
    'product.public.category', 'search_read',[[('name','=',categ['name'])]],{'offset': 0, 'limit': 1})
            if public_categs:
                template['public_categ_ids'].append(public_categs[0]['id'])
        


    del template['image_small']
    del template['image']
    del template['image_medium']
    del template['event_template_id']
    del template['ticket_id']
    del template['incoming_qty_pack']
    del template['property_valuation']
    del template['onhand_stock']
    del template['reservation_count']
    del template['description_variant']
    del template['track_service']
    del template['virtual_available_pack']
    del template['property_cost_method']
    del template['event_type_id']
    del template['property_stock_account_input']
    del template['message_last_post']
    del template['qv_description_variant']
    del template['company_ids']
    del template['mo_count']
    del template['state']
    del template['website_style_ids']
    del template['purchase_count']
    del template['warranty']
    del template['quote_description']
    del template['product_manager']
    del template['x_groups']
    del template['product_brand_id']
    del template['forest_stock']
    del template['item_ids']
    del template['outgoing_qty_pack']
    del template['property_stock_account_output']
    del template['qty_available_pack']
    del template['rental']
    del template['tag_ids']
    del template['property_stock_procurement']
    del template['product_variant_ids']
    del template['taxes_id']
    del template['supplier_taxes_id']
    del template['message_follower_ids']
    del template['message_partner_ids']
    del template['message_ids']
    del template['website_message_ids']
    del template['message_channel_ids']
    del template['wk_product_pack']
    del template['is_pack']
    del template['project_id']
    del template['create_uid']
    del template['write_uid']

    del template['attribute_line_ids']
    del template['seller_ids']
    del template['alternative_product_ids']
    del template['accessory_product_ids']
    
    
    
    # del template['task_id']

    # print(template)

    id = models_v_14.execute_kw(db_v_14, uid_v_14, password_v_14, 'product.template', 'create', [template])
    models_v_14.execute_kw(db_v_14, uid_v_14, password_v_14, 'product.template', 'write', [[id], {
        'list_price': template['list_price']
    }])
    print("Processed template id [%s] %s of %s [%s] %s"%(id, i, size, 100 * i/size, '%'))

