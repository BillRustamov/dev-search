from django.urls import path

from .import views

app_name = 'main'

urlpatterns = [
    path('', views.ProjectsListView.as_view(), name='home'),

    path('project/<str:pk>/', views.project_detail, name='project_detail'),
    path('add-project/', views.add_project, name='add_project'),
    path('edit-project/<str:pk>/', views.edit_project, name='edit_project'),
    path('delete-project/<str:pk>/', views.delete_project, name='delete_project'),
]
