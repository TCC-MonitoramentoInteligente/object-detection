from django.urls import path

from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('unregister/', views.unregister, name='unregister'),
    path('status/', views.status, name='status'),
    path('print/', views.event_print, name='print'),
    path('monitor/', views.monitor, name='monitor'),
]
