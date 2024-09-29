from django.urls import path

from .import views

urlpatterns = [
    path('register/',views.register_page,name = 'register_page'),
    path('login/',views.login_page,name = 'login_page'),
    path('home/',views.home,name = 'home'),
    path('logout/',views.logout_page,name = 'logout_page'),
    path('password_reset/',views.password_reset,name = 'password_reset'),
    path('change_password/<str:username>/',views.change_password,name = 'change_password'),
    path('taskflow/home/',views.TaskFlowHome,name = 'TaskFlowHome'),
    path('taskflow/todo_list/',views.todo_list,name = 'todo_list'),
    path('tasksflow/task_update/<int:id>/',views.task_update,name = 'task_update'),
    path('taskflow/taskflow/delete/<int:id>/',views.delete_task,name = 'delete_task'),
]
