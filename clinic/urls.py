from django.urls import path
from . import views

app_name = 'clinic'

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:obj>/new/', views.new_obj, name='new'),
    path('<str:obj>/<pk>/', views.view_obj, name='view'),
    path('logout/', views.logout, name='logout'),
]
