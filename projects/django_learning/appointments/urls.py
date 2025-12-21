from django.urls import path

from appointments import views
from appointments.views import schedule_views, talon_views, doctor_views
from appointments.views.doctor_views import doctors_list_view, doctor_detail_view
from appointments.views.home_view import home_view

urlpatterns = [
    path('', home_view, name='home'),

    # Doctor URLs
    path('doctors/', doctor_views.doctors_list_view, name='doctors_list'),
    path('doctors/<int:doctor_id>/', doctor_views.doctor_detail_view, name='doctor_detail'),
    path('doctors/<int:doctor_id>/talons/', talon_views.doctor_talons_view, name='doctor_talons'),

    # Schedule URLs
    path('schedules/', schedule_views.schedules_view, name='schedules'),
    path('schedules/create/', schedule_views.create_schedule_view, name='create_schedule'),
    path('schedules/<int:schedule_id>/generate-talons/', schedule_views.generate_talons_view, name='generate_talons'),

    # Talon URLs
    path('talons/', talon_views.talons_view, name='talons'),
    path('talons/create/', talon_views.create_talon_view, name='create_talon'),
    path('talons/<int:talon_id>/', talon_views.talon_detail_view, name='talon_detail'),
    path('talons/<int:talon_id>/book/', talon_views.book_talon_view, name='book_talon'),
    path('talons/<int:talon_id>/cancel/', talon_views.cancel_talon_view, name='cancel_talon'),
]