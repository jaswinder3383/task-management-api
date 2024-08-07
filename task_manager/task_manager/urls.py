"""task_manager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin


from django.urls import path, include
from tasks import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/register/', views.register_user, name='register'),
    path('api/login/', views.login_user, name='login'),
    path('api/tasks/', views.TaskListCreateAPIView.as_view(), name='task-list-create'),
    path('api/tasks/<int:pk>/', views.TaskDetailAPIView.as_view(), name='task-detail'),
    path('api/tasks/<int:pk>/members/', views.TaskMemberAPIView.as_view(), name='task-members'),
    path('api/tasks/<int:pk>/add-remove-task-member/', views.add_remove_task_member, name='add-remove-task-member'),
    # path('api/tasks/<int:pk>/remove-member/', views.remove_task_member, name='remove-task-member'),
    path('api/tasks/<int:pk>/comments/', views.add_task_comment, name='add-task-comment'),
    path('api/tasks/<int:pk>/update-status/', views.update_task_status, name='update-task-status'),
]
