import xmlrpc.client


#v14
url_v_14 = 'http://odoov12ent.boxed.cz'
db_v_14 = 'boxed'
username_v_14 = 'admin2@boxed.cz'
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
users = models_v_9.execute_kw(db_v_9, uid_v_9, password_v_9,
    'res.users', 'search_read',[[]],{'offset': offset, 'limit': size,
    'fields': ['name', 'image_small','image_medium','firstname',
    'lastname', 'partner_id','login_date','lang','tz','notification_type',
    'signature','login']})

for i, user in enumerate(users):
    i = i+1
    print(user)
    user['image_1920'] = user['image_small']
    if user['partner_id']:
        partner_id = user['partner_id'][0]
        if partners := models_v_14.execute_kw(
            db_v_14,
            uid_v_14,
            password_v_14,
            'res.partner',
            'search_read',
            [[('database_id_v9', '=', partner_id)]],
        ):
            user['partner_id'] = partners[0]['id']
        else:
            del user['partner_id']
    del user['image_small']
    print(f"Processing [{user['id']}] {i} of {size} [{100 * i / size}] %")
    id = models_v_14.execute_kw(db_v_14, uid_v_14, password_v_14, 'res.users', 'create', [user])

    print(f"Processed user id [{id}] {i} of {size} [{100 * i / size}] %")

