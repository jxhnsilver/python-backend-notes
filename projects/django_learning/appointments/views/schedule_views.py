# appointments/views/schedule_views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from ..models import Schedule, Doctor, Clinic, Talon
from ..services.schedule_service import split_schedule_to_talons
from datetime import datetime


def schedules_view(request):
    """Список всех графиков - GET /schedules/"""
    schedules = Schedule.objects.all().select_related('doctor', 'clinic').order_by('-date', 'start_time')

    # Для каждого расписания получаем талоны
    for schedule in schedules:
        schedule.talons = Talon.objects.filter(
            doctor=schedule.doctor,
            date=schedule.date
        ).order_by('start_time')

    return render(request, 'schedules/index.html', {
        'schedules': schedules,
        'page_title': 'Расписания'
    })


def create_schedule_view(request):
    """Создание графика - GET/POST /schedules/create/"""
    if request.method == 'POST':
        try:
            doctor_id = request.POST.get('doctor_id')
            date_str = request.POST.get('date')
            start_time_str = request.POST.get('start_time')
            end_time_str = request.POST.get('end_time')
            start_break_str = request.POST.get('start_break_time')
            end_break_str = request.POST.get('end_break_time')
            clinic_id = request.POST.get('clinic_id')

            # Конвертируем строки в даты/время
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
            start_time = datetime.strptime(start_time_str, '%H:%M').time()
            end_time = datetime.strptime(end_time_str, '%H:%M').time()
            start_break_time = datetime.strptime(start_break_str, '%H:%M').time()
            end_break_time = datetime.strptime(end_break_str, '%H:%M').time()

            doctor = get_object_or_404(Doctor, id=doctor_id)
            clinic = get_object_or_404(Clinic, id=clinic_id)

            # Создаем график
            schedule = Schedule.objects.create(
                clinic=clinic,
                doctor=doctor,
                date=date,
                start_time=start_time,
                end_time=end_time,
                start_break_time=start_break_time,
                end_break_time=end_break_time
            )

            # Автоматически создаем талоны из графика
            created_talons = split_schedule_to_talons(schedule.id)

            messages.success(
                request,
                f"График создан успешно! Создано {len(created_talons)} талонов."
            )
            return redirect('schedules')

        except Exception as e:
            messages.error(request, f"Ошибка при создании графика: {str(e)}")

    # GET запрос - показываем форму
    doctors = Doctor.objects.all()
    clinics = Clinic.objects.all()

    return render(request, 'schedules/create.html', {
        'doctors': doctors,
        'clinics': clinics
    })


def generate_talons_view(request, schedule_id):
    """Создание талонов из графика - POST /schedules/{id}/generate-talons/"""
    try:
        created_talons = split_schedule_to_talons(schedule_id)
        return JsonResponse({
            'success': True,
            'message': f'Создано {len(created_talons)} талонов',
            'talon_count': len(created_talons)
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=400)