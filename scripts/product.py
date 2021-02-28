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
size = 1 - done
offset = 0 + done
print('Offset:', offset)
templates = models_v_9.execute_kw(db_v_9, uid_v_9, password_v_9,
    'product.template', 'search_read',[[]],{'offset': offset, 'limit': size})

for i, template in enumerate(templates):
    i = i+1
    print(template)
    del template['image_small']
    del template['image']
    del template['image_medium']
    print(template)
    template['image_1024'] = template['image_small']
    template['image_1920'] = template['image']
    template['currency_id'] = 9

    del template['image_small']
    del template['image']
    del template['event_template_id']

    
    print("Processing [%s] %s of %s [%s] %s"%(template['id'], i, size, 100 * i/size, '%'))

