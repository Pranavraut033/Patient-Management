from django.urls import path, re_path
from . import views
from . import test
app_name = 'clinic'
handler404 = 'clinic.views.handler404'

urlpatterns = [
    # re_path(r'$', views.er_404, name='er_404'),
    # path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    # path('add/<str:object>/', views.add_object, name='add'),
    # path('test',test.a,name='test'),
    # # path('<str:object>/<str:pk>/', views.view_object, name='view'),
    # path('logout/', views.logout, name='logout'),
]
