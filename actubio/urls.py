
from django.urls import path
from .import views

urlpatterns = [

    path('AB_login/',views.AB_login),
    path('AB_home/',views.AB_home),
    path('AB_logout/',views.AB_logout),
    path('BA_Record/',views.BA_Record),
    path('AB_Process/',views.AB_Process),
    path('actubio_process/<str:c_id>/', views.actubio_process),
    path('actu_bio_report/',views.actu_bio_report),

]
