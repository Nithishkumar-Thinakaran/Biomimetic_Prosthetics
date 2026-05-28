
from django.urls import path
from .import views

urlpatterns = [
    path('IH_login/',views.IH_login),
    path('IH_home/',views.IH_home),
    path('IH_logout/',views.IH_logout),
    path('client_record/',views.client_record),
    path('integration_process/<str:c_id>/',views.integration_process),
    path('integration/',views.integration),
    path('IH_Report/',views.IH_Report),

]
