from django.shortcuts import render, redirect, HttpResponse
from tasks.models import *
from tasks.forms import TaskForm, TasklistForm, CommentForm, Subtaskform
from appmethods import create_task, create_tasklist, modelsearch, add_users
from django.contrib import auth
from django.contrib.auth.decorators import login_required


def logout_view(request):
    auth.logout(request)
    return redirect('tasks:index')


@login_required
def index(request):
    if request.method == 'GET':
        taskform = TaskForm()
        tasklistform = TasklistForm()
        all_tasks = TasksModel.objects.all().filter(parent_id=None)
        tasklists = TaskList.user_objects.get(request.user.id)
        orphan_tasks = TasksModel.objects.filter(tasklist_id=None)
        user_role= UserModel.objects.get(user=request.user.id).user_role
        return render(request, 'tasks/index.html',
                      context={'all_tasks': all_tasks, 'tasklists': tasklists, 'taskform': taskform,
                               'tasklistform': tasklistform, 'orphan_tasks': orphan_tasks,'role':user_role})
    if request.method == 'POST':
        formname = request.POST['formname']
        if formname == 'task':
            exitcode = create_task(request.POST)
            if exitcode == 0:
                return redirect('tasks:index')
            elif exitcode == 255:
                taskform = TaskForm(request.POST)
                return redirect('tasks:index')
        elif formname == 'tasklist':
            exitcode = create_tasklist(request.POST)
            if exitcode == 0:
                return redirect('tasks:index')
            elif exitcode == 255:
                tasklistform = TasklistForm(request.POST)
                return redirect('tasks:index')


@login_required
def taskview(request, id):
    if request.method == 'GET':
        task = TasksModel.objects.get(id=id)
        comments = CommentsModel.objects.filter(task_id=id)
        commentform = CommentForm()
        tasklists = TaskList.objects.all()
        taskform = TaskForm(instance=task)
        subtaskform = Subtaskform()
        user_role= UserModel.objects.get(user=request.user.id).user_role
        is_allowed = TasklistUserModel.objects.filter(tasklist_id=task.tasklist_id, user_id=request.user)
        sub_tasks = TasksModel.objects.filter(parent_id=id)
        if task.parent_id:
            parent = TasksModel.objects.get(id=task.parent_id)
        else:
            parent = None
        if len(is_allowed) or user_role != 'employee':
            return render(request, 'tasks/task.html',
                      context={'task': task, 'comments': comments, 'commentform': commentform, 'taskform': taskform,
                               'tasklists': tasklists, 'subtaskform': subtaskform, 'role': user_role,
                               'subtasks': sub_tasks, 'parent': parent})
        else:
            return HttpResponse("You dont have permissions to view this page.")

    if request.method == 'POST':
        task = TasksModel.objects.get(id=id)
        try:
            formname = request.POST['formname']
        except:
            formname = None
        if formname == 'task':
            exitcode = create_task(request.POST, method='edit', instance=task)
            if exitcode == 0:
                return redirect('tasks:taskview', id)
            elif exitcode == 255:
                taskform = TaskForm(request.POST)
                return HttpResponse(taskform.errors)
        elif formname is None:
            commentform = CommentForm(request.POST)
            if commentform.is_valid():
                comment_text = commentform.cleaned_data['comment']
                comment = CommentsModel(task_id=task, comment=comment_text)
                comment.save()
            return redirect('tasks:taskview', id)


@login_required
def tasklistview(request, id):
    if request.method == 'GET':
        if id == '0':
            tasks = TasksModel.objects.filter(tasklist_id=None)
            return render(request, 'tasks/orphan_tasks.html', context={'tasks': tasks})
        else:
            tasklist = TaskList.objects.get(id=id)
            tasklistform = TasklistForm(instance=tasklist)
            tasks = TasksModel.objects.filter(tasklist_id=id)
            user_role = UserModel.objects.get(user=request.user.id).user_role
            is_allowed=TasklistUserModel.objects.filter(tasklist_id=tasklist,user_id=request.user)
            usersshared = [UserModel.objects.get(user=i.user_id) for i in
                           TasklistUserModel.objects.filter(tasklist_id=tasklist)]
            usersshared = list(set(usersshared))
            users = list(set(UserModel.objects.all()))
            for user in usersshared:
                if user in users:
                    users.remove(user)

            if len(is_allowed) or user_role != 'employee':
                return render(request, 'tasks/tasklist.html',
                              context={'tasklist': tasklist, 'tasklistform': tasklistform, 'tasks': tasks,'users':users,
                                       'role': user_role, 'usersshared': usersshared,})
            else:
                return HttpResponse("You dont have permissions to view this page.")
    if request.method == 'POST':
        tasklist = TaskList.objects.get(id=id)
        try:
            formname = request.POST['formname']
        except:
            formname = None
        if formname == 'tasklist':
            exitcode = create_tasklist(request.POST, method='edit', instance=tasklist)
            if exitcode == 0:
                return redirect('tasks:tasklistview', id)
            elif exitcode == 255:
                tasklistform = TasklistForm(request.POST)
                return HttpResponse(tasklistform.errors)
        elif formname == 'addusers':
            exitcode=add_users(request.POST,id)
            return redirect('tasks:tasklistview', id)


@login_required
def search(request):
    query = None
    if 'query' in request.POST:
        query = request.POST['query']
    if query is not None and len(query.strip()) != 0:
        context = modelsearch(query)
        return render(request, 'tasks/search.html', context=context)
    else:
        return redirect('tasks:index')


@login_required
def subtasksretrive(request, id):
    if request.method == 'GET':
        task = TasksModel.objects.get(id=id)
        return render(request, 'tasks/subtasks.html', context={})
    if request.method == 'POST':
        try:
            subtask1 = TasksModel.objects.filter(parent_id=id)
            return render(request, 'tasks/subtasks.html', context={"subtasks": subtask1})
        except:
            return render(request, 'tasks/dialog.html', context={"msg": "No SubTasks exist"})

    return


@login_required
def addsubtask(request):
    if request.method == 'POST':
        tasklist_id = request.POST['tasklist_id']
        taskform = Subtaskform()
        parentid = request.POST['parentid']
        exitcode = create_task(request.POST, 'subtask')
        return redirect('tasks:taskview', parentid)
