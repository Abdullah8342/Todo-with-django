from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404

from django.contrib import messages

from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout

from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User

from django.http import HttpResponse


from .models import Todo
from .forms import FormTodo

# Create your views here.

# registration page
def register_page(request):
    if request.method == 'POST':
        first_name = request.POST.get('f_name')
        last_name = request.POST.get('l_name')
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = User.objects.filter(username = username)
        if user.exists():
            messages.info(request,'Username already taken')
            return redirect('register_page')
        user = User.objects.create_user(
            username = username,
            first_name = first_name,
            last_name = last_name,
        )
        user.set_password(password)
        user.save()
        messages.info(request,'Account created successfully')
        return redirect('login_page')
    return render(request,'safe_sign/register.html')

def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = User.objects.get(username = username)
        if not user.DoesNotExist():
            messages.error(request,'Invalid Username')
            return HttpResponse('lgoin_page')
        user = authenticate(username = username,password = password)

        if user is None:
            messages.error(request,'Invalid password')
            return redirect('login_page')
        else:
            login(request,user)
            return redirect('TaskFlowHome') # return to Task home page
    return render(request,'safe_sign/login.html')


# password reset vew
def password_reset(request):
    if request.method == 'POST':
        username = request.POST.get('username')

        try:
            user = User.objects.get(username = username)
        except user.DoesNotExist():
            return HttpResponse('Invalid Username')
        username = user.username
        return redirect('change_password',username = username)
    return render(request,'safe_sign/password_reset.html')

def change_password(request,username):
    if request.method == 'POST':
        password = request.POST.get('password')
        user = User.objects.get(username = username)
        user.set_password(password)
        user.save()
        return redirect('login_page')
    return render(request,'safe_sign/change_password.html')


@login_required
def home(request):
    # find the username and the id of the loged user
    if request.user.is_authenticated:
        username = request.user.username
        id = request.user.id
    else:
        username = None
        id = None
    return render(request,'safe_sign/home.html',{'username1':username,'id':id})

@login_required
def logout_page(request):
    logout(request)
    return redirect('login_page')


# Taskflow

@login_required
def TaskFlowHome(request):
    if request.method == 'POST':
        form = FormTodo(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            todo_status = form.cleaned_data['todo_status']
            # return HttpResponse(f'{title} {description} {todo_status} {request.user.id}')
            todo = Todo(title = title,description = description)
            todo.todo_status = todo_status
            todo.user = User.objects.get(id=request.user.id)
            todo.save()
        return redirect('todo_list')
    form = FormTodo()
    return render(request,'taskflow/home.html',{'form':form})

def todo_list(request):
    if request.user.is_authenticated:
        user_id = request.user.id
        data = Todo.objects.filter(user = user_id)
        return render(request,'taskflow/list.html',{'data':data})
    else:
        return render(request,'taskflow/list.html',{'data':'Empty lsit'})

def task_update(request,id):
    user_id = request.user.id
    item = get_object_or_404(Todo,id = id ,user_id = user_id)
    if request.method == 'POST':
        form = FormTodo(request.POST,instance=item)
        if form.is_valid():
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            todo_status = form.cleaned_data['todo_status']
            todo = Todo(id = id ,title = title,description = description,todo_status = todo_status)
            todo.user = User.objects.get(id=request.user.id)
            todo.save()
        return redirect('todo_list')
    form = FormTodo(instance=item)
    return render(request,'taskflow/update.html',{'form':form})


def delete_task(request,id):
    item = Todo.objects.get(id = id)
    item.delete()
    return redirect('todo_list')
