from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.home, name='home'),
    path('home/<uuid:id>/', views.home, name='home_with_id'),
    path('login/', views.login, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/<uuid:id>/', views.dashboard, name='dashboard_with_id'),
    path('student/', views.student, name='student'),
    path('student/<uuid:id>/', views.student, name='student_with_id'),
    path('manage/', views.manage, name='manage'),
    path('manage/<uuid:id>/', views.manage, name='manage_with_id'),
    path('logout/', views.logout, name='logout'),
    path('submit_attendance/<uuid:id>/', views.submit_attendance, name='submit_attendance'),
    path('export_as_csv/<uuid:id>/', views.export_as_csv, name='export_as_csv'),
    path('session/<uuid:id>/', views.session_management, name='session'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)