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
packs = models_v_9.execute_kw(db_v_9, uid_v_9, password_v_9,
    'product.pack', 'search_read',[[]],{'offset': offset, 'limit': size})


for i, pack in enumerate(packs):
    pack['product_id'] = pack['product_name']
    del pack['product_name']

    if pack['wk_product_template']:
        wk_product_template = models_v_14.execute_kw(db_v_14, uid_v_14, password_v_14,
        'product.template', 'search_read',[[('database_id_v9','=',pack['wk_product_template'][0])]],{'offset': 0, 'limit': 1})
        if wk_product_template:
            wk_product_template = wk_product_template[0]['id']
            pack['wk_product_template'] = wk_product_template
    
            if pack['product_id']:
                product_id = models_v_14.execute_kw(db_v_14, uid_v_14, password_v_14,
                'product.product', 'search_read',[[('name','=',pack['product_id'][1])]],{'offset': 0, 'limit': 1})
                if product_id:
                    product_id = product_id[0]['id']
                    pack['product_id'] = product_id
                    # print(pack)
                    id = models_v_14.execute_kw(db_v_14, uid_v_14, password_v_14, 'product.pack', 'create', [pack])
                    models_v_14.execute_kw(db_v_14, uid_v_14, password_v_14, 'product.template', 'write', [[pack['wk_product_template']], {
                        'is_pack': True
                    }])
                    print("Processed pack id [%s] %s of %s [%s] %s"%(id, i, size, 100 * i/size, '%'))
