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
size = 1#1000 - done
offset = 0 + done
print('Offset:', offset)

events = models_v_9.execute_kw(db_v_9, uid_v_9, password_v_9,
    'event.event', 'search_read',[[]],{'offset': offset, 'limit': size})

for i, event in enumerate(events):
    i = i+1
    print(f"Processing [{event['id']}] {i} of {size} [{100 * i / size}] %")
    event['database_id_v9'] = event['id']
    event['country_id'] = 56

    if event['user_id']:
        try:
            user = models_v_9.execute_kw(db_v_9, uid_v_9, password_v_9,
                'res.users', 'search_read',[[('id','=',event['user_id'][0])]],{'limit': size})[0]
            event['user_id'] = models_v_14.execute_kw(db_v_14, uid_v_14, password_v_14,
            'res.users', 'search',[[('login','=',user['login'])]],{'limit': size})[0]
        except:
            event['user_id'] = uid_v_14

    if event['organizer_id']:
        if partner_id := models_v_14.execute_kw(
            db_v_14,
            uid_v_14,
            password_v_14,
            'res.partner',
            'search_read',
            [[('database_id_v9', '=', event['organizer_id'][0])]],
            {'limit': size},
        ):
            event['organizer_id'] = partner_id[0]['id']
        else:
            event['organizer_id'] = False

    if event['address_id']:
        if partner_id := models_v_14.execute_kw(
            db_v_14,
            uid_v_14,
            password_v_14,
            'res.partner',
            'search_read',
            [[('database_id_v9', '=', event['address_id'][0])]],
            {'limit': size},
        ):
            event['address_id'] = partner_id[0]['id']
        else:
            event['address_id'] = False

    if event['company_id']:
        company_id = models_v_14.execute_kw(db_v_14, uid_v_14, password_v_14,
            'res.company', 'search',[[('name','=',event['company_id'][1])]],{'limit': size})
        event['company_id'] = company_id[0]


    del event['event_template_id']
    del event['sale_order_origin']
    del event['task_id']
    del event['joined_sale_order_ids']
    del event['sale_order_line_origin']
    del event['event_type_id']
    del event['event_ticket_ids']

    # event['event_template_id']
    # sale_order_origin
    # task_id
    # joined_sale_order_ids
    #sale_order_line_origin



    del event['message_last_post']
    del event['count_sponsor']
    del event['twitter_hashtag']
    del event['state']
    del event['seats_min']
    del event['show_blog']
    del event['show_menu']
    del event['show_track_proposal']
    del event['blog_id']
    del event['color']
    del event['count_tracks']
    del event['reply_to']
    del event['show_tracks']
    del event['seats_availability']
    del event['registration_ids']
    del event['message_partner_ids']
    del event['message_ids']
    del event['message_follower_ids']
    del event['survey_id']
    del event['specific_question_ids']
    del event['accreditation_id']
    del event['website_message_ids']
    # del event['blog_id']
    # del event['blog_id']
    # del event['blog_id']
    # del event['blog_id']
    # del event['blog_id']
    # del event['blog_id']
    # del event['blog_id']
    # del event['blog_id']
    # del event['blog_id']
    # del event['blog_id']


    print(event)
    id = models_v_14.execute_kw(db_v_14, uid_v_14, password_v_14, 'event.event', 'create', [event])

    print(f"Processed [{event['id']}] {i} of {size} [{100 * i / size}] %")
