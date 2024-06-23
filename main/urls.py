from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('editprofile/', views.editprofile, name='editprofile'),
    path('passchange/', views.passchange, name='passchange'),
    path('doctor/', views.doctor, name='doctor'),
    path('patient/', views.patient, name='patient'),
    path('history/', views.Viewhistory, name='viewhistory'),
    path('addhistory/', views.addhistory, name='addhistory'),
    path('health/', views.health, name='health'),
    path('appointment/<int:aptId>', views.appointment, name='appointment'),
    path('Viewappointment/', views.viewappointments, name='viewappointments'),
    path('Delappointment/<int:aptId>', views.deleteappointment, name='deleteappointment'),
    path('plans/', views.plans, name='plans'),
    path('report/', views.report, name='report'),
    path('feedback/', views.feedback, name='feedback'),
    path('viewfeedback/', views.viewfeedback, name='viewfeedback'),
    path('polls/', views.polls, name='polls'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)