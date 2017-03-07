from django.contrib.auth.models import Group, Permission
from django.apps import apps as django_apps

apps_add_change_permissions = [
    {'bcpp_subject': ['add', 'change']},
    {'plot': ['add', 'change']},
    {'household': ['add', 'change']},
    {'member': ['add', 'change']}
]
action_manager_exclude = [{
    'bcpp_subject': {
        'denyall': ['livewith'], 'deny': [('', 'change')]}}
]
assistant_project_coord_exclude = []
clinic_research_assistant_exclude = []
comm_liaison_officer_exclude = []
data_manager_exclude = []
field_research_assistant_exclude = []
IT_admin_exclude = []
IT_assistant_exclude = []
lab_assistant_exclude = []
report_exclude = []

groups = {
    'action_manager': {
        'give': apps_add_change_permissions,
        'deny': action_manager_exclude},
    'assistant_project_coord': {
        'give': apps_add_change_permissions,
        'deny': assistant_project_coord_exclude},
    'clinic_research_assistant': {
        'give': apps_add_change_permissions,
        'deny': clinic_research_assistant_exclude},
    'comm_liaison_officer': {
        'give': apps_add_change_permissions,
        'deny': data_manager_exclude},
    'data_manager': {
        'give': apps_add_change_permissions,
        'deny': action_manager_exclude},
    'field_research_assistant': {
        'give': apps_add_change_permissions,
        'deny': field_research_assistant_exclude},
    'field_supervisor': {
        'give': apps_add_change_permissions,
        'deny': field_research_assistant_exclude},
    'IT_admin': {
        'give': apps_add_change_permissions,
        'deny': IT_admin_exclude},
    'IT_assistant': {
        'give': apps_add_change_permissions,
        'deny': IT_assistant_exclude},
    'lab_assistant': {
        'give': apps_add_change_permissions,
        'deny': lab_assistant_exclude},
    'reports': {
        'give': apps_add_change_permissions,
        'deny': report_exclude}
}

for group_name in groups.keys():
    try:
        Group.objects.get(name=group_name)
    except Group.DoesNotExist:
        Group.objects.create(name=group_name)

for group_name in list(groups.keys()):
    give = groups.get(group_name).get('give')
    deny = groups.get(group_name).get('deny')
    group = Group.objects.get(name=group_name)
    for g in give:
        app_label = list(g)[0]
        permissions = g.get(app_label, [])
        app = django_apps.get_app_config(app_label)
        for model in app.get_models():
            for p in permissions:
                code_name = '{}_{}'.format(p, model._meta.model_name)
                try:
                    group.permissions.get(codename=code_name)
                except Permission.DoesNotExist:
                    try:
                        permission = Permission.objects.get(codename=code_name)
                        group.permissions.add(permission)
                    except Permission.MultipleObjectsReturned:
                        for p in Permission.objects.filter(codename=code_name):
                            group.permissions.add(permission)
