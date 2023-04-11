import xmlrpc.client


#v14
url_v_14 = 'http://odoov12ent.boxed.cz'
db_v_14 = 'boxed'
username_v_14 = 'admin@boxed.cz'
password_v_14 = '1Juzepe1'
port_v_14 = '8069'
common_v_14 = xmlrpc.client.ServerProxy(
    f'{url_v_14}:{port_v_14}/xmlrpc/2/common'
)
uid_v_14 = common_v_14.authenticate(db_v_14, username_v_14, password_v_14, {})
models_v_14 = xmlrpc.client.ServerProxy(
    f'{url_v_14}:{port_v_14}/xmlrpc/2/object'
)
print(uid_v_14)

#v9
url_v_9 = 'https://portal.boxed.cz'
db_v_9 = 'boxed'
username_v_9 = 'admin@boxed.cz'
password_v_9 = '1Juzepe1'
port_v_9 = '443'
common_v_9 = xmlrpc.client.ServerProxy(f'{url_v_9}:{port_v_9}/xmlrpc/2/common')
uid_v_9 = common_v_9.authenticate(db_v_9, username_v_9, password_v_9, {})
models_v_9 = xmlrpc.client.ServerProxy(f'{url_v_9}:{port_v_9}/xmlrpc/2/object')
print(uid_v_9)

done = 0
size = 1000 - done
offset = 0 + done
print('Offset:', offset)

orders = models_v_9.execute_kw(db_v_9, uid_v_9, password_v_9,
    'sale.order', 'search_read',[[]],{'offset': offset, 'limit': size})

for i, order in enumerate(orders):
    i = i+1
    print(f"Processing [{order['id']}] {i} of {size} [{100 * i / size}] %")
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
        if partner_id := models_v_14.execute_kw(
            db_v_14,
            uid_v_14,
            password_v_14,
            'res.partner',
            'search_read',
            [[('database_id_v9', '=', order['partner_id'][0])]],
            {'limit': size},
        ):
            order['partner_id'] = partner_id[0]['id']
        else:
            order['partner_id'] = False

    if order['partner_invoice_id']:
        if partner_id := models_v_14.execute_kw(
            db_v_14,
            uid_v_14,
            password_v_14,
            'res.partner',
            'search_read',
            [[('database_id_v9', '=', order['partner_invoice_id'][0])]],
            {'limit': size},
        ):
            order['partner_invoice_id'] = partner_id[0]['id']
        else:
            order['partner_invoice_id'] = False

    if order['partner_shipping_id']:
        if partner_id := models_v_14.execute_kw(
            db_v_14,
            uid_v_14,
            password_v_14,
            'res.partner',
            'search_read',
            [[('database_id_v9', '=', order['partner_shipping_id'][0])]],
            {'limit': size},
        ):
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
        if task_ids := models_v_14.execute_kw(
            db_v_14,
            uid_v_14,
            password_v_14,
            'project.task',
            'search',
            [[('database_id_v9', 'in', order['tasks_ids'])]],
            {'limit': size},
        ):
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
    order_line_ids = order['order_line']
    del order['order_line']
    order_id = models_v_14.execute_kw(db_v_14, uid_v_14, password_v_14, 'sale.order', 'create', [order])


    # print('order_line_ids', order_line_ids)
    # order_lines = models_v_9.execute_kw(db_v_9, uid_v_9, password_v_9,
    # 'sale.order.line', 'search_read',[[('id','in',order_line_ids)]],{'offset': 0, 'limit': 1000})

    # for line in order_lines:
    #     line['database_id_v9'] = line['id']
    #     line['order_partner_id'] = order['partner_id']
    #     line['currency_id'] = order['currency_id']
    #     line['company_id'] = order['company_id']
    #     line['order_id'] = order_id
    #     if line['product_uom']:
    #         line['product_uom'] = line['product_uom'][0]
        
    #     if line['product_id']:
    #         product_id = models_v_14.execute_kw(db_v_14, uid_v_14, password_v_14,
    #         'product.product', 'search_read',[[('name','=',line['product_id'][1])]],{'limit': size})
    #         if product_id:
    #             line['product_id'] = product_id[0]['id']
    #         else:
    #             line['product_id'] = False
    #     # if line['product_tmpl_id']:
    #     #     product_tmpl_id = models_v_14.execute_kw(db_v_14, uid_v_14, password_v_14,
    #     #     'product.template', 'search_read',[[('database_id_v9','=',line['product_tmpl_id'][0])]],{'limit': size})
    #     #     if product_tmpl_id:
    #     #         line['product_tmpl_id'] = product_tmpl_id[0]['id']
    #     #     else:
    #     #         line['product_tmpl_id'] = False
        
    #     # salesman_id
    #     if line['salesman_id']:
    #         try:
    #             user = models_v_9.execute_kw(db_v_9, uid_v_9, password_v_9,
    #                 'res.users', 'search_read',[[('id','=',line['salesman_id'][0])]],{'limit': size})[0]
    #             line['salesman_id'] = models_v_14.execute_kw(db_v_14, uid_v_14, password_v_14,
    #             'res.users', 'search',[[('login','=',user['login'])]],{'limit': size})[0]
    #         except:
    #             line['salesman_id'] = False
        
        
    #     del line['event_ticket_id']
    #     del line['attendee_ids']
    #     del line['invoice_lines']
    #     del line['procurement_ids']
    #     del line['reservation_ids']
    #     del line['event_id']
    #     del line['option_line_id']
    #     del line['product_pack_count']
    #     del line['event_type_id']
    #     del line['qty_delivered_updateable']
    #     del line['discounted_price']
    #     del line['is_low_forecast']
    #     del line['is_low_stock']
    #     del line['is_stock_reservable']
    #     del line['x_bseprice']
    #     del line['product_tmpl_id']
    #     del line['property_ids']
    #     # del line['is_low_forecast']
    #     # del line['is_low_forecast']
    #     # del line['is_low_forecast']
        

    #     # print(line)
    #     line_id = models_v_14.execute_kw(db_v_14, uid_v_14, password_v_14, 'sale.order.line', 'create', [line])

    print(f"Processed [{order_id}] {i} of {size} [{100 * i / size}] %")