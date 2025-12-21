# appointments/views/talon_views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from ..models import Talon, Doctor
from ..services.talon_service import book_talon, cancel_talon
from datetime import datetime


def talons_view(request):
    """Список всех талонов - GET /talons/"""
    talons = Talon.objects.all().select_related('doctor').order_by('date', 'start_time')

    return render(request, 'talons/index.html', {
        'talons': talons,
        'page_title': 'Талоны'
    })


def doctor_talons_view(request, doctor_id):
    """Талоны конкретного врача - GET /doctors/{id}/talons/"""
    doctor = get_object_or_404(Doctor, id=doctor_id)
    talons = Talon.objects.filter(doctor=doctor).select_related('doctor').order_by('date', 'start_time')

    return render(request, 'talons/index.html', {
        'talons': talons,
        'doctor': doctor,
        'page_title': f'Талоны врача {doctor.full_name}'
    })


def talon_detail_view(request, talon_id):
    """Детали талона - GET /talons/{id}/"""
    talon = get_object_or_404(Talon, id=talon_id)

    return render(request, 'talons/detail.html', {
        'talon': talon,
        'page_title': f'Талон #{talon.id}'
    })


def book_talon_view(request, talon_id):
    """Забронировать талон - POST /talons/{id}/book/"""
    try:
        talon = book_talon(talon_id)
        messages.success(request, f"Талон #{talon_id} успешно забронирован!")
        return redirect('talon_detail', talon_id=talon_id)
    except Exception as e:
        messages.error(request, str(e))
        return redirect('talon_detail', talon_id=talon_id)


def cancel_talon_view(request, talon_id):
    """Отменить бронирование талона - POST /talons/{id}/cancel/"""
    try:
        talon = cancel_talon(talon_id)
        messages.success(request, f"Бронирование талона #{talon_id} отменено")
        return redirect('talon_detail', talon_id=talon_id)
    except Exception as e:
        messages.error(request, str(e))
        return redirect('talon_detail', talon_id=talon_id)


def create_talon_view(request):
    """Создать талон вручную - GET/POST /talons/create/"""
    if request.method == 'POST':
        try:
            doctor_id = request.POST.get('doctor_id')
            date_str = request.POST.get('date')
            start_time_str = request.POST.get('start_time')
            end_time_str = request.POST.get('end_time')

            # Исправьте формат строк!
            # Было: '%YYYY-%mM-%dd' и '%HH:%MM' - это неверно
            # Должно быть: '%Y-%m-%d' и '%H:%M'
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
            start_time = datetime.strptime(start_time_str, '%H:%M').time()
            end_time = datetime.strptime(end_time_str, '%H:%M').time()

            doctor = Doctor.objects.get(id=doctor_id)

            # Создаем талон
            talon = Talon.objects.create(
                doctor=doctor,
                date=date,
                start_time=start_time,
                end_time=end_time,
                is_free=True
            )

            messages.success(request, "Талон создан успешно!")
            return redirect('talon_detail', talon_id=talon.id)

        except Exception as e:
            messages.error(request, f"Ошибка при создании талона: {str(e)}")

    # GET запрос
    doctors = Doctor.objects.all()
    return render(request, 'talons/create.html', {
        'doctors': doctors
    })
