
from django.urls import path
from .import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admins_login/',views.admins_login),
    path('admins_logout/',views.admins_logout),
    path('admins_home/',views.admins_home),
    path('client_reg/',views.client_reg),
    path('approve/<int:id>/',views.approve),
    path('reject/<int:id>/',views.reject),

    #Integrate Hub
    path('IH_Result/',views.IH_Result),

    #Bio Analysis
    path('BA_Result/',views.BA_Result),

    #Actu-Bio
    path('AB_Result/',views.AB_Result),

    path('authorize_report/',views.authorize_report),

    path('view_final_report/<str:c_id>/',views.view_final_report),

    path('finalreportapprove/<str:c_id>/',views.finalreportapprove),

    path('finalreportreject/<str:c_id>/',views.finalreportreject)
]
urlpatterns += static(settings.MEDIA_URL,document_root=settings
                      .MEDIA_ROOT)
