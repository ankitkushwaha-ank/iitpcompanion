from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from IITP_copanion_plus import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('assignment/', views.assignment, name='Assignment'),
    path('search/', views.search_view, name='search'),
    path('contact-us/', views.contact_view, name='contact'),
    path('test/', views.test, name='test'),
    path('progress/', views.progress, name='progress'),
    path('auth/login/', views.login, name='login'),
    path('auth/register/', views.register, name='register'),
    path('auth/logout/', views.logout, name='logout'),
    path('feedback/', views.feedback, name='feedback'),
    path('maps/', views.maps, name='maps'),
    path('student_clubs/', views.student_clubs, name='student_clubs'),
    path('clubs/<slug:slug>/', views.club_detail, name='club_detail'),
    path('events/', views.events, name='events'),
    path('events/save/', views.save_event, name='save_event'),
    path('events/api/', views.get_events, name='get_events'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('notifications/mark-read/', views.mark_notifications_read, name='mark_notifications_read'),
    path('events/delete/<int:event_id>/', views.delete_event, name='delete_event'),
    path('about/', views.about_us, name='about'),
    path('restaurant/', views.restaurant, name='restaurant'),
    path('assignment/', views.assignment, name='assignment'),
    path('subscribe/', views.subscribe, name='subscribe'),
    path('toggle-status/', views.toggle_assignment_status, name='toggle_assignment_status'),
    path('profile/', views.profile_view, name='profile'),
    path('leave-club/<int:club_id>/', views.leave_club, name='leave_club'),
    path('register-event/<int:event_id>/', views.register_event, name='register_event'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),

    path('tracker/', views.tracker_view, name='tracker'),
    path('profile/change-password/', views.change_password, name='change_password'),
    path('owner/', include('Restaurant.urls')),
    path('food/', include('Orderfood.urls')),

    path('<path>/', views.errorpage, name='error'),
    path('<path>/<err>/', views.errorpage2, name='error2'),
    path('<path>/<err>/<errr>/', views.errorpage3, name='error3'),



]

# Static and media files (for development)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
