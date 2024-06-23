from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('passchange/', views.passchange, name='passchange'),
    path('doctor/', views.doctor, name='doctor'),
    path('patient/', views.patient, name='patient'),
    path('health/', views.health, name='health'),
    path('appointment/<int:aptId>', views.appointment, name='appointment'),
    path('report/', views.report, name='report'),
    path('feedback/', views.feedback, name='feedback'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)