
from django.urls import path
from .import views

urlpatterns = [
    path('',views.index),
    path('client_signup_login/',views.client_signup_login),
    path('client_home/',views.client_home),
    path('client_login/',views.client_login),
    path('client_logout/',views.client_logout),
    path('client_req/',views.client_req),
    path('checkpoints/',views.checkpoints),

]
