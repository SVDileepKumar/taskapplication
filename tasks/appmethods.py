from tasks.models import TaskList, TasksModel, CommentsModel, UserModel,TasklistUserModel
from tasks.forms import TaskForm, TasklistForm
from django.contrib.auth.models import User


def create_task(form_data, method='create', instance=None):
    taskform = TaskForm(form_data)
    if taskform.is_valid():
        name = taskform.cleaned_data['name']
        description = taskform.cleaned_data['description']
        status = taskform.cleaned_data['completion_status']
        start_date = form_data['start_date']
        if start_date == '':
            start_date = None
        end_date = form_data['end_date']
        if end_date == '':
            end_date = None
        if start_date > end_date:
            start_date = None
            end_date = None
        try:
            tasklist_id = form_data['tasklist_id']
            mytaklist = TaskList.objects.get(id=tasklist_id)
        except:
            mytaklist = None
        parentid = None
        if method == 'subtask':
            parentid = form_data['parentid']

        if method == 'create' or method == 'subtask':
            if start_date is None or end_date is None:
                task = TasksModel(name=name, description=description, completion_status=status,
                                  tasklist_id=mytaklist, parent_id=parentid, root_id=parentid)
                task.save()
            else:
                task = TasksModel(name=name, description=description, completion_status=status,
                                  tasklist_id=mytaklist, start_date=start_date, end_date=end_date, parent_id=parentid,
                                  root_id=parentid)
                task.save()

        elif method == 'edit':
            task = TasksModel.objects.get(id=instance.id)
            task.name = name
            task.description = description
            task.completion_status = status
            if start_date is not None and end_date is not None:
                task.start_date = start_date
                task.end_date = end_date
            if mytaklist is not None:
                task.tasklist_id = mytaklist
            task.save()
        return 0
    return 255


def create_tasklist(form_data, method='create', instance=None):
    tasklistform = TasklistForm(form_data)
    if tasklistform.is_valid():
        name = tasklistform.cleaned_data['name']
        try:
            description = tasklistform.cleaned_data['description']
        except:
            description = None
        try:
            notes = tasklistform.cleaned_data['notes']
        except:
            notes = None
        status = tasklistform.cleaned_data['status']
        if method == 'create':
            tasklist = TaskList(name=name, description=description, notes=notes, status=status)
            tasklist.save()
        elif method == 'edit':
            tasklist = TaskList.objects.get(id=instance.id)
            tasklist.name = name
            tasklist.description = description
            tasklist.notes = notes
            tasklist.status = status
            tasklist.save()
        return 0
    return 255


def modelsearch(query):
    all_tasklists = TaskList.user_objects.all()
    all_tasks = TasksModel.objects.all()
    tasks = list(all_tasks.filter(name__icontains=query))
    for task in tasks:
        all_tasks.exclude(id=task.id)
    tasks_description = all_tasks.filter(description__icontains=query)
    for task in tasks_description:
        all_tasks.exclude(id=task.id)
    comments = CommentsModel.objects.filter(comment__icontains=query)
    tasks_comments = list(set([i.task_id for i in comments]))
    tasklists = list(all_tasklists.filter(name__icontains=query))
    for tasklist in tasklists:
        all_tasklists.exclude(id=tasklist.id)
    tasklists_description = all_tasklists.filter(description__icontains=query)
    for tasklist in tasklists_description:
        all_tasklists.exclude(id=tasklist.id)
    tasklists_notes = all_tasklists.filter(notes__icontains=query)
    total_tasks = len(tasks) + len(tasks_description) + len(tasks_comments)
    total_tasklists = len(tasklists) + len(tasklists_description) + len(tasklists_notes)
    context = {'tasks': tasks, 'tasklists': tasklists,
               'tasks_description': tasks_description, 'tasks_comments': tasks_comments,
               'tasklists_description': tasklists_description, 'tasklists_notes': tasklists_notes,
               'tasks_number': total_tasks, 'tasklists_number': total_tasklists, 'query': query, 'comments': comments
               }
    return context


def add_users(formdata,tasklist_id):
    tasklist=TaskList.objects.get(id=tasklist_id)
    ids = formdata.getlist('adduser')
    for id in ids:
        user = User.objects.get(id=id)
        customuser=TasklistUserModel(user_id=user,tasklist_id=tasklist)
        customuser.save()
    return 0
