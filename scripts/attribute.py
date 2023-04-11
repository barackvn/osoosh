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

done = 11
size = 1000 - done
offset = 0 + done
print('Offset:', offset)
attributes = models_v_9.execute_kw(db_v_9, uid_v_9, password_v_9,
    'product.attribute.line', 'search_read',[[]],{'offset': offset, 'limit': size})

{'id': 7, 'value_ids': [29, 28], 
'__last_update': '2018-08-27 09:24:36', 
'write_uid': [1, 'Administrator'], 
'attribute_id': [2, 'Barva'], 
'create_uid': [1, 'Administrator'], 
'display_name': 'Barva', 
'product_tmpl_id': [6, 'Multifunkční stojan 40" - 55"']}



for i, attribute in enumerate(attributes):
    i = i+1
    # attribute['display_type'] = attribute['type']

    # del attribute['color']
    # del attribute['price_extra']
    # del attribute['product_ids']
    # del attribute['price_ids']
    print('Attribute', attribute)
    if attribute['attribute_id']:
        attribute_id = models_v_14.execute_kw(db_v_14, uid_v_14, password_v_14,
        'product.attribute', 'search_read',[[('name','=',attribute['attribute_id'][1])]],{'offset': 0, 'limit': 1})[0]['id']
        attribute['attribute_id'] = attribute_id

    if attribute['product_tmpl_id']:
        if product_tmpl_id := models_v_14.execute_kw(
            db_v_14,
            uid_v_14,
            password_v_14,
            'product.template',
            'search_read',
            [[('database_id_v9', '=', attribute['product_tmpl_id'][0])]],
            {'offset': 0, 'limit': 1},
        ):
            product_tmpl_id = product_tmpl_id[0]['id']
            attribute['product_tmpl_id'] = product_tmpl_id

    if attribute['value_ids']:
        values = models_v_9.execute_kw(db_v_9, uid_v_9, password_v_9,
        'product.attribute.value', 'search_read',[[('id','in',attribute['value_ids'])]],{'offset': 0, 'limit': 100})
        value_ids = []
        print('VALUES', values)
        for v in values:
            if value_id := models_v_14.execute_kw(
                db_v_14,
                uid_v_14,
                password_v_14,
                'product.attribute.value',
                'search_read',
                [[('name', '=', v['name'])]],
                {'offset': 0, 'limit': 1},
            ):
                value_id = value_id[0]['id']
                # [0]['id']
                value_ids.append(value_id)
        attribute['value_ids'] = value_ids
    try:
        id = models_v_14.execute_kw(db_v_14, uid_v_14, password_v_14, 'product.template.attribute.line', 'create', [attribute])
        print(f"Processing [{attribute['id']}] {i} of {size} [{100 * i / size}] %")
    except Exception as e:
        print(e)
