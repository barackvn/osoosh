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

# done = 5+29+52+20+157
done = 0 #107+157+36+34+664 for #1000  #166+22+42+283+112 for 0###
size = 1000 - done
offset = 7000 + done
print('Offset:', offset)

# tags = models_v_9.execute_kw(db_v_9, uid_v_9, password_v_9,
#     'project.tags', 'search_read',[[]],{'offset': 0, 'limit': 1000})

# for i, tag in enumerate(tags):
#     i = i+1
#     # del p_type['case_default']
#     # del p_type['autostaging_enabled']
#     # del p_type['legend_priority']
#     # del p_type['closed']
#     # del p_type['autostaging_idle_timeout']
#     # del p_type['autostaging_next_stage']
#     # del p_type['legend_blocked']
#     # del p_type['legend_normal']
#     # del p_type['legend_done']
#     # del p_type['project_ids']
#     # del p_type['rating_template_id']
#     # del p_type['survey_id']

    
#     print("Processing [%s] %s of %s [%s] %s"%(tag['id'], i, size, 100 * i/size, '%'))
#     tag['database_id_v9'] = tag['id']
#     print(tag)
#     id = models_v_14.execute_kw(db_v_14, uid_v_14, password_v_14, 'project.tags', 'create', [tag])

#     print("Processed [%s] %s of %s [%s] %s"%(tag['id'], i, size, 100 * i/size, '%'))



# types = models_v_9.execute_kw(db_v_9, uid_v_9, password_v_9,
#     'project.task.type', 'search_read',[[]],{'offset': offset, 'limit': size})

# for i, p_type in enumerate(types):
#     i = i+1
#     del p_type['case_default']
#     del p_type['autostaging_enabled']
#     del p_type['legend_priority']
#     del p_type['closed']
#     del p_type['autostaging_idle_timeout']
#     del p_type['autostaging_next_stage']
#     del p_type['legend_blocked']
#     del p_type['legend_normal']
#     del p_type['legend_done']
#     del p_type['project_ids']
#     del p_type['rating_template_id']
#     del p_type['survey_id']

    
#     print("Processing [%s] %s of %s [%s] %s"%(p_type['id'], i, size, 100 * i/size, '%'))
#     p_type['database_id_v9'] = p_type['id']
#     print(p_type)
#     id = models_v_14.execute_kw(db_v_14, uid_v_14, password_v_14, 'project.task.type', 'create', [p_type])

#     print("Processed [%s] %s of %s [%s] %s"%(p_type['id'], i, size, 100 * i/size, '%'))



# projects = models_v_9.execute_kw(db_v_9, uid_v_9, password_v_9,
#     'project.project', 'search_read',[['|',('active','=',True),('active','=',False)]],{'offset': offset, 'limit': size})

# for i, project in enumerate(projects):
#     i = i+1
#     print("Processing [%s] %s of %s [%s] %s"%(project['id'], i, size, 100 * i/size, '%'))
#     project['database_id_v9'] = project['id']
#     project['currency_id'] = 9

#     if project['type_ids']:
#         type_ids = models_v_14.execute_kw(db_v_14, uid_v_14, password_v_14,
#     'project.task.type', 'search',[[('database_id_v9','in',project['type_ids'])]],{'offset': offset, 'limit': size})
#         project['type_ids'] = type_ids

#     del project['members']
#     del project['use_issues']
#     del project['debit']
#     del project['project_ids']
#     del project['code']
#     del project['is_visible_happy_customer']
#     del project['task_needaction_count']
#     del project['state']
#     del project['percentage_satisfaction_task']
#     del project['balance']
#     del project['line_ids']
#     del project['credit']
#     del project['issue_count']
#     del project['percentage_satisfaction_project']
#     del project['message_last_post']
#     del project['alias_model']
#     del project['issue_needaction_count']
#     del project['label_issues']
#     del project['vuente_tags']
#     del project['project_count']
#     del project['task_team_ids']
#     del project['team_id']
#     del project['use_timesheets']
#     del project['tag_ids']
#     del project['use_tasks']
#     del project['percentage_satisfaction_issue']
#     del project['account_type']
#     del project['issue_ids']
#     del project['autostaging_enabled']
#     del project['company_uom_id']
#     del project['alias_parent_model_id']
#     del project['tasks']
#     del project['message_ids']
#     del project['task_ids']
#     del project['message_follower_ids']
#     del project['website_message_ids']
#     del project['company_id']
#     del project['analytic_account_id']
#     del project['alias_id']
#     del project['message_partner_ids']
#     del project['alias_model_id']
#     del project['message_channel_ids']
#     del project['create_uid']
#     del project['write_uid']
#     del project['user_id']
#     del project['resource_calendar_id']
    
#     print(project)
#     id = models_v_14.execute_kw(db_v_14, uid_v_14, password_v_14, 'project.project', 'create', [project])

#     print("Processed [%s] %s of %s [%s] %s"%(project['id'], i, size, 100 * i/size, '%'))

tasks = models_v_9.execute_kw(db_v_9, uid_v_9, password_v_9,
    'project.task', 'search_read',[['|',('active','=',True),('active','=',False),('stage_id','!=',11)]],{'offset': offset, 'limit': size})

for i, task in enumerate(tasks):
    i = i+1
    print("Processing [%s] %s of %s [%s] %s"%(task['id'], i, size, 100 * i/size, '%'))
    task['database_id_v9'] = task['id']
    # project['currency_id'] = 9

    if task['project_id']:
        project_id = models_v_14.execute_kw(db_v_14, uid_v_14, password_v_14,
    'project.project', 'search',[[('database_id_v9','=',task['project_id'][0])]],{'limit': size})
        print(project_id)
        task['project_id'] = project_id[0]

    
    if task['stage_id']:
        stage_id = models_v_14.execute_kw(db_v_14, uid_v_14, password_v_14,
    'project.task.type', 'search',[[('database_id_v9','=',task['stage_id'][0])]],{'limit': size})
        task['stage_id'] = stage_id[0]
    
    if task['partner_id']:
        print(task['partner_id'])
        partner_id = models_v_14.execute_kw(db_v_14, uid_v_14, password_v_14,
    'res.partner', 'search_read',[[('database_id_v9','=',task['partner_id'][0])]],{'limit': size})
        if partner_id:
            task['partner_id'] = partner_id[0]['id']
        else:
            task['partner_id'] = False
    
    if task['product_id']:
        product_id = models_v_14.execute_kw(db_v_14, uid_v_14, password_v_14,
    'product.product', 'search_read',[[('name','=',task['product_id'][1])]],{'limit': size})
        if product_id:
            task['product_id'] = product_id[0]['id']
        else:
            task['product_id'] = False
    
    if task['company_id']:
        company_id = models_v_14.execute_kw(db_v_14, uid_v_14, password_v_14,
    'res.company', 'search_read',[[('name','=',task['company_id'][1])]],{'limit': size})
        task['company_id'] = company_id[0]['id']
    
    if task['users_id']:
        users = models_v_9.execute_kw(db_v_9, uid_v_9, password_v_9,
            'res.users', 'search_read',[[('id','in',task['users_id'])]],{'limit': size})
        task['users_ids'] = list()
        for user in users:
            user_id = models_v_14.execute_kw(db_v_14, uid_v_14, password_v_14,
        'res.users', 'search',[[('login','=',user['login'])]],{'limit': size})
            task['users_ids'].extend(user_id)
    
    if task['tag_ids']:
        tag_ids = models_v_14.execute_kw(db_v_14, uid_v_14, password_v_14,
        'project.tags', 'search',[[('database_id_v9','in',task['tag_ids'])]],{'limit': size})
        if tag_ids:
            task['tag_ids'] = tag_ids
        else:
            task['tag_ids'] = False
    
    del task['users_id']
    del task['reminder_event_id']
    del task['survey_result_ids']
    del task['event_ids']
    del task['manager_id']
    del task['survey_id']
    del task['message_ids']
    del task['timesheet_ids']
    del task['response_id']
    del task['reminder_alarm_ids']
    del task['child_ids']
    del task['message_channel_ids']
    del task['sale_line_id']
    del task['procurement_id']
    del task['message_partner_ids']
    del task['joined_event_ids']
    del task['message_follower_ids']
    del task['rating_ids']
    del task['total_hours']
    del task['delay_hours']
    del task['date_start']
    del task['autostaging_days_left']
    del task['message_last_post']
    del task['autostaging_next_stage']
    del task['task_url']
    del task['autostaging_date']
    del task['notes']
    del task['autostaging_enabled']
    del task['pri']
    del task['parent_ids']
    del task['website_message_ids']
#     del task['message_ids']
#     del task['task_ids']
#     del task['message_follower_ids']
#     del task['website_message_ids']
#     del task['company_id']
    del task['analytic_account_id']
#     del project['alias_id']
#     del project['message_partner_ids']
#     del project['alias_model_id']
#     del project['message_channel_ids']
#     del project['create_uid']
#     del project['write_uid']
#     del project['user_id']
#     del project['resource_calendar_id']
    
    # print(task)
    try:
        id = models_v_14.execute_kw(db_v_14, uid_v_14, password_v_14, 'project.task', 'create', [task])

        print("Processed [%s] %s of %s [%s] %s"%(task['id'], i, size, 100 * i/size, '%'))
    except Exception as e:
        print(e)

