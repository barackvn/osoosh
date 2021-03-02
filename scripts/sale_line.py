
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

    for line in order_lines:
        line['database_id_v9'] = line['id']
        line['order_partner_id'] = order['partner_id']
        line['currency_id'] = order['currency_id']
        line['company_id'] = order['company_id']
        line['order_id'] = order_id

        if line['order_id']:
            order_id = models_v_14.execute_kw(db_v_14, uid_v_14, password_v_14,
                'sale.order', 'search',[[('database_id_v9','=',line['order_id'][0])]],{'limit': 1})
            if order_id:
                line['order_id'] = order_id[0]
            else:
                continue

        if line['product_uom']:
            line['product_uom'] = line['product_uom'][0]
        
        if line['product_id']:
            product_id = models_v_14.execute_kw(db_v_14, uid_v_14, password_v_14,
            'product.product', 'search_read',[[('name','=',line['product_id'][1])]],{'limit': size})
            if product_id:
                line['product_id'] = product_id[0]['id']
            else:
                line['product_id'] = False
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
        

        # print(line)
        line_id = models_v_14.execute_kw(db_v_14, uid_v_14, password_v_14, 'sale.order.line', 'create', [line])

    print("Processed [%s] %s of %s [%s] %s"%(line_id, i, size, 100 * i/size, '%'))