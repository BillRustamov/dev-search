from django.urls import path

from .import views

app_name = 'users'

urlpatterns = [
    path('', views.ProfilesListView.as_view(), name='home'),

    path('inbox/', views.inbox, name='inbox'),
    path('message/<int:pk>/', views.message_detail, name='message_detail'),
    path('send-message/<str:pk>/', views.send_message, name='send_message'),

    path('account/<str:pk>/', views.account_detail, name='account_detail'),
    path('account-update/', views.account_update, name='account_update'),
    path('account/', views.account, name='account'),

    path('add-skill/', views.add_skill, name='add_skill'),
    path('edit-skill/<str:pk>/', views.edit_skill, name='edit_skill'),
    path('delete-skill/<str:pk>/', views.delete_skill, name='delete_skill'),

    path('signin/', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
    path('signout/', views.signout, name='signout'),
]
