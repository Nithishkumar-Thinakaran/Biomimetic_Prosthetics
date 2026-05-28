
from django.urls import path
from .import views

urlpatterns = [
    path('BA_login/',views.BA_login),
    path('BA_home/',views.BA_home),
    path('BA_logout/',views.BA_logout),
    path('IntegrateHub_Report/',views.IntegrateHub_Report),
    path('bioanalysis/',views.bioanalysis),
    path('bioanalysis_process/<str:c_id>/',views.bioanalysis_process),
    path('bioanalysis_report/',views.bioanalysis_report),

]
