# appointments/views/doctor_views.py
from django.shortcuts import render, get_object_or_404
from django.http import Http404
from ..models import Doctor, Talon
from ..services.doctor_service import get_doctors, get_doctor_by_id


def doctors_list_view(request):
    """Список врачей - GET /doctors/"""
    doctors = get_doctors()
    context = {
        'doctors': doctors,
        'total_count': len(doctors),
        'page_title': 'Список врачей',
    }
    return render(request, 'doctors/index.html', context)


def doctor_detail_view(request, doctor_id: int):
    """Детали врача - GET /doctors/{id}/"""
    doctor = get_doctor_by_id(doctor_id)
    if not doctor:
        raise Http404("Doctor not found")

    # Получаем талоны врача
    talons = Talon.objects.filter(doctor=doctor).order_by('date', 'start_time')

    context = {
        'doctor': doctor,
        'talons': talons,
        'page_title': f'Доктор {doctor.full_name}',
    }
    return render(request, 'doctors/detail.html', context)