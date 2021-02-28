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
size = 1#1000 - done
offset = 0 + done
print('Offset:', offset)
projects = models_v_9.execute_kw(db_v_9, uid_v_9, password_v_9,
    'project.project', 'search_read',[['|',('active','=',True),('active','=',False)]],{'offset': offset, 'limit': size})

for i, project in enumerate(projects):
    i = i+1
    print("Processing [%s] %s of %s [%s] %s"%(project['id'], i, size, 100 * i/size, '%'))
    project['database_id_v9'] = project['id']
    project['currency_id'] = 9

    del project['members']
    del project['use_issues']
    del project['debit']
    del project['project_ids']
    del project['code']
    del project['is_visible_happy_customer']
    del project['task_needaction_count']
    del project['state']
    del project['percentage_satisfaction_task']
    del project['balance']
    del project['line_ids']
    del project['credit']
    del project['issue_count']
    del project['percentage_satisfaction_project']
    del project['message_last_post']
    del project['alias_model']
    del project['issue_needaction_count']
    del project['label_issues']
    del project['vuente_tags']
    del project['project_count']
    del project['task_team_ids']
    del project['team_id']
    del project['use_timesheets']
    del project['tag_ids']
    del project['use_tasks']
    del project['percentage_satisfaction_issue']
    del project['account_type']
    del project['issue_ids']
    del project['autostaging_enabled']
    del project['company_uom_id']
    del project['alias_parent_model_id']
    del project['tasks']
    del project['message_ids']
    del project['task_ids']
    del project['message_follower_ids']
    del project['website_message_ids']
    del project['company_id']
    del project['analytic_account_id']
    del project['alias_id']
    del project['message_partner_ids']
    del project['alias_model_id']
    del project['message_channel_ids']
    del project['create_uid']
    del project['write_uid']
    del project['user_id']

    
    del project['type_ids'] 
    

    print(project)
    id = models_v_14.execute_kw(db_v_14, uid_v_14, password_v_14, 'project.project', 'create', [project])

    print("Processed [%s] %s of %s [%s] %s"%(project['id'], i, size, 100 * i/size, '%'))

