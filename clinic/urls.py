from django.urls import path, re_path
from . import views
from . import test
app_name = 'clinic'
handler404 = 'clinic.views.handler404'

urlpatterns = [
    # re_path(r'$', views.er_404, name='er_404'),
    path('', views.index, name='index'),
    path('logout/', views.logout, name='logout'),
	path('add/<str:model>', views.add, name="add"),
<<<<<<< HEAD
    path('view/<str:model>/<int:pk>', views.view, name='view'),
=======
    # path('add/<str:object>/', views.add_object, name='add'),
>>>>>>> 5ab21846fc6691c11e626fe83a36c178362f9805
    # path('test',test.a,name='test'),
    # # path('<str:object>/<str:pk>/', views.view_object, name='view'),
]
