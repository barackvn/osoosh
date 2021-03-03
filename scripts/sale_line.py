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

done = 0
size = 1000 - done
offset = 0 + done
print('Offset:', offset)

order_lines = models_v_9.execute_kw(db_v_9, uid_v_9, password_v_9,
'sale.order.line', 'search_read',[[]],{'offset': offset, 'limit': size})

for i, line in enumerate(order_lines):
    i = i+1
    print("Processing [%s] %s of %s [%s] %s"%(line['id'], i, size, 100 * i/size, '%'))
    #print(line)
    
    line['database_id_v9'] = line['id']
    if line['order_partner_id']:
        partner_id = models_v_14.execute_kw(db_v_14, uid_v_14, password_v_14,
            'res.partner', 'search_read',[[('database_id_v9','=',line['order_partner_id'][0])]],{'limit': size})
        if partner_id:
            line['order_partner_id'] = partner_id[0]['id']
        else:
            line['order_partner_id'] = False
    line['currency_id'] = 9
    if line['tax_id']:
        line['tax_id'] = [(6, 0, line['tax_id'])]
   
    if line['company_id']:
        company_id = models_v_14.execute_kw(db_v_14, uid_v_14, password_v_14,
            'res.company', 'search',[[('name','=',line['company_id'][1])]],{'limit': size})
        line['company_id'] = company_id[0]
    
    if line['order_id']:
        order_id = models_v_14.execute_kw(db_v_14, uid_v_14, password_v_14,
            'sale.order', 'search',[[('database_id_v9','=',line['order_id'][0])]],{'limit': 1})
        if order_id:
            line['order_id'] = order_id[0]
        else:
            orders = models_v_9.execute_kw(db_v_9, uid_v_9, password_v_9,
                'sale.order', 'search_read',[[('id','=',line['order_id'][0])]],{'offset': offset, 'limit': size})
            for order in orders:
                order['database_id_v9'] = order['id']
                # order['message_partner_ids'] = 9
                # order['country_id'] = 56
                order['currency_id'] = 9
                order['team_id'] = 1
                order_line_ids = order['order_line']

                if order['payment_term_id']:
                    order['payment_term_id'] = order['payment_term_id'][0]
                if order['pricelist_id']:
                    order['pricelist_id'] = order['pricelist_id'][0]
                if order['template_id']:
                    order['template_id'] = order['template_id'][0]
                    
                

                if order['tag_ids']:
                    tags = models_v_9.execute_kw(db_v_9, uid_v_9, password_v_9,
                        'crm.order.tag', 'search_read',[[('id','in',order['tag_ids'])]],{'limit': size})
                    order['tag_ids'] = []
                    for tag in tags:
                        tag_id = models_v_14.execute_kw(db_v_14, uid_v_14, password_v_14,
                        'crm.tag', 'search',[[('name','=',tag['name'])]],{'limit': size})[0]
                        order['tag_ids'].append(tag_id)
                
                if order['company_id']:
                    company_id = models_v_14.execute_kw(db_v_14, uid_v_14, password_v_14,
                        'res.company', 'search',[[('name','=',order['company_id'][1])]],{'limit': size})
                    order['company_id'] = company_id[0]
                
                if order['user_id']:
                    try:
                        user = models_v_9.execute_kw(db_v_9, uid_v_9, password_v_9,
                            'res.users', 'search_read',[[('id','=',order['user_id'][0])]],{'limit': size})[0]
                        order['user_id'] = models_v_14.execute_kw(db_v_14, uid_v_14, password_v_14,
                        'res.users', 'search',[[('login','=',user['login'])]],{'limit': size})[0]
                    except:
                        order['user_id'] = False

                if order['partner_id']:
                    partner_id = models_v_14.execute_kw(db_v_14, uid_v_14, password_v_14,
                        'res.partner', 'search_read',[[('database_id_v9','=',order['partner_id'][0])]],{'limit': size})
                    if partner_id:
                        order['partner_id'] = partner_id[0]['id']
                    else:
                        order['partner_id'] = False
                
                if order['partner_invoice_id']:
                    partner_id = models_v_14.execute_kw(db_v_14, uid_v_14, password_v_14,
                        'res.partner', 'search_read',[[('database_id_v9','=',order['partner_invoice_id'][0])]],{'limit': size})
                    if partner_id:
                        order['partner_invoice_id'] = partner_id[0]['id']
                    else:
                        order['partner_invoice_id'] = False
                
                if order['partner_shipping_id']:
                    partner_id = models_v_14.execute_kw(db_v_14, uid_v_14, password_v_14,
                        'res.partner', 'search_read',[[('database_id_v9','=',order['partner_shipping_id'][0])]],{'limit': size})
                    if partner_id:
                        order['partner_shipping_id'] = partner_id[0]['id']
                    else:
                        order['partner_shipping_id'] = False
                
                
                # if order['opportunity_id']:
                #     opportunity_id = models_v_14.execute_kw(db_v_14, uid_v_14, password_v_14,
                #         'crm.lead', 'search_read',[[('database_id_v9','=',order['opportunity_id'][0])]],{'limit': size})
                #     if opportunity_id:
                #         order['opportunity_id'] = opportunity_id[0]['id']
                #     else:
                #         order['opportunity_id'] = False
                
                if order['tasks_ids']:
                    task_ids = models_v_14.execute_kw(db_v_14, uid_v_14, password_v_14,
                        'project.task', 'search',[[('database_id_v9','in',order['tasks_ids'])]],{'limit': size})
                    if task_ids:
                        order['tasks_ids'] = task_ids
                    else:
                        order['tasks_ids'] = []
                        


                del order['message_partner_ids']
                del order['event_ids']
                del order['source_id']
                del order['invoice_ids']
                del order['attendee_ids']
                del order['message_ids']
                del order['warehouse_id']
                del order['website_message_ids']
                del order['message_channel_ids']
                del order['medium_id']
                del order['message_follower_ids']
                del order['options']
                del order['has_stock_reservation']
                del order['x_admin_backend']
                del order['template_id']
                del order['message_last_post']
                del order['payment_tx_id']
                del order['payment_acquirer_id']
                del order['has_delivery']
                del order['invoice_shipping_on_delivery']
                del order['is_stock_reservable']
                del order['requested_date']
                del order['attachment_count']
                del order['x_executive_date']
                del order['quote_viewed']
                del order['product_id']
                del order['delivery_price']
                del order['procurement_group_id']
                del order['opportunity_id']
                # del order['order_line']
                del order['joined_event_ids']
                del order['cancel_reason_id']
                # del order['options']
                # del order['options']
                # del order['options']
                # del order['options']
                # del order['options']
                # del order['options']
                # del order['options']
                # del order['options']

                # print(order)
                del order['order_line']
                line['order_id'] = models_v_14.execute_kw(db_v_14, uid_v_14, password_v_14, 'sale.order', 'create', [order])
                print('Created Order')
            print('No order_id')
            

    if line['product_uom']:
        line['product_uom'] = line['product_uom'][0]
    
    if line['product_id']:
        product_id = models_v_14.execute_kw(db_v_14, uid_v_14, password_v_14,
        'product.product', 'search',[[('name','=',line['product_tmpl_id'][1])]],{'limit': size})
        if product_id:
            line['product_id'] = product_id[0]
        else:
            line['product_id'] = False
            templates = models_v_9.execute_kw(db_v_9, uid_v_9, password_v_9,
                'product.product', 'search_read',[[]],{'offset': offset, 'limit': size})

            for i, template in enumerate(templates):
                i = i+1
                print("Processing [%s] %s of %s [%s] %s"%(template['id'], i, size, 100 * i/size, '%'))

                # del template['image_small']
                # del template['image']
                # del template['image_medium']
                template['database_id_v9'] = template['id']
                template['image_512'] = template['image_small']
                template['image_1920'] = template['image']
                template['image_1024'] = template['image_medium']
                template['combination_indices'] = False
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
                
                if template['product_tmpl_id']:
                    product_tmpl_id = models_v_14.execute_kw(db_v_14, uid_v_14, password_v_14,
                'product.template', 'search_read',[[('database_id_v9','=',template['product_tmpl_id'][0])]],{'offset': 0, 'limit': 1})
                    if product_tmpl_id:
                        template['product_tmpl_id'] = product_tmpl_id[0]['id']
                    


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
                del template['name_template']
                del template['reception_count']
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

                del template['company_id']
                del template['attribute_line_ids']
                del template['seller_ids']
                del template['alternative_product_ids']
                del template['accessory_product_ids']
                del template['related_product_ids']
                del template['attribute_value_ids']
                del template['delivery_count']
                del template['image_variant']
                # del template['delivery_count']
                # del template['delivery_count']
                # del template['delivery_count']
                # del template['delivery_count']
                # del template['delivery_count']
                
                
                
                # del template['task_id']

                # print(template)

                line['product_id'] = models_v_14.execute_kw(db_v_14, uid_v_14, password_v_14, 'product.product', 'create', [template])
                models_v_14.execute_kw(db_v_14, uid_v_14, password_v_14, 'product.product', 'write', [[id], {
                    'list_price': template['list_price']}])
                print('Created Product')
            print('No product')
            
    # if line['product_tmpl_id']:
    #     product_tmpl_id = models_v_14.execute_kw(db_v_14, uid_v_14, password_v_14,
    #     'product.template', 'search_read',[[('database_id_v9','=',line['product_tmpl_id'][0])]],{'limit': size})
    #     if product_tmpl_id:
    #         line['product_tmpl_id'] = product_tmpl_id[0]['id']
    #     else:
    #         line['product_tmpl_id'] = False
    
    # salesman_id
    if line['salesman_id']:
        try:
            user = models_v_9.execute_kw(db_v_9, uid_v_9, password_v_9,
                'res.users', 'search_read',[[('id','=',line['salesman_id'][0])]],{'limit': size})[0]
            line['salesman_id'] = models_v_14.execute_kw(db_v_14, uid_v_14, password_v_14,
            'res.users', 'search',[[('login','=',user['login'])]],{'limit': size})[0]
        except:
            line['salesman_id'] = False
            print('No salesman_id')
    
    
    del line['event_ticket_id']
    del line['attendee_ids']
    del line['invoice_lines']
    del line['procurement_ids']
    del line['reservation_ids']
    del line['event_id']
    del line['option_line_id']
    del line['product_pack_count']
    del line['event_type_id']
    del line['qty_delivered_updateable']
    del line['discounted_price']
    del line['is_low_forecast']
    del line['is_low_stock']
    del line['is_stock_reservable']
    del line['x_bseprice']
    del line['product_tmpl_id']
    del line['property_ids']
    # del line['is_low_forecast']
    # del line['is_low_forecast']
    # del line['is_low_forecast']
    

    print(line)
    line_id = models_v_14.execute_kw(db_v_14, uid_v_14, password_v_14, 'sale.order.line', 'create', [line])

    print("Processed [%s] %s of %s [%s] %s"%(line_id, i, size, 100 * i/size, '%'))