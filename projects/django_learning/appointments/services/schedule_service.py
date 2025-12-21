# appointments/services/schedule_service.py
from datetime import datetime, time, timedelta
from ..models import Schedule, Talon, Doctor
from typing import List
from django.db import transaction


def split_schedule_to_talons(schedule_id: int) -> List[Talon]:
    """
    Разбивает график врача на талоны по длительности приема
    Проверяет пересечения с существующими ЗАНЯТЫМИ талонами
    Создает только свободные талоны
    """
    try:
        schedule = Schedule.objects.get(id=schedule_id)
    except Schedule.DoesNotExist:
        raise ValueError(f"Расписание с id {schedule_id} не найдено")

    doctor = schedule.doctor
    duration_minutes = doctor.duration
    schedule_date = schedule.date

    # Конвертируем время в datetime
    start_datetime = datetime.combine(schedule_date, schedule.start_time)
    end_datetime = datetime.combine(schedule_date, schedule.end_time)
    start_break_datetime = datetime.combine(schedule_date, schedule.start_break_time)
    end_break_datetime = datetime.combine(schedule_date, schedule.end_break_time)

    # Генерируем временные слоты
    time_slots = []
    current_time = start_datetime

    while current_time < end_datetime:
        # Проверяем, начинается ли текущий слот в перерыве
        if start_break_datetime <= current_time < end_break_datetime:
            # Перескакиваем на конец перерыва
            current_time = end_break_datetime
            continue

        # Рассчитываем конец слота
        slot_end = current_time + timedelta(minutes=duration_minutes)

        # Проверяем, не выходит ли слот за конец рабочего дня
        if slot_end > end_datetime:
            break

        # Проверяем, не попадает ли конец слота в перерыв
        if start_break_datetime < slot_end <= end_break_datetime:
            # Если слот заканчивается в перерыве, обрезаем его до начала перерыва
            slot_end = start_break_datetime
            if slot_end <= current_time:
                # Если после обрезки ничего не осталось, переходим к следующему
                current_time = end_break_datetime
                continue

        # Проверяем, не начинается ли слот до перерыва, а заканчивается после
        if current_time < start_break_datetime and slot_end > end_break_datetime:
            # Разбиваем на два слота: до перерыва и после
            # Создаем слот до перерыва
            time_slots.append({
                'start_time': current_time.time(),
                'end_time': start_break_datetime.time(),
                'date': schedule_date,
                'doctor': doctor
            })
            # Перескакиваем после перерыва
            current_time = end_break_datetime
            continue

        # Проверяем, не пересекается ли слот с перерывом
        if current_time < end_break_datetime and slot_end > start_break_datetime:
            # Пропускаем перерыв
            current_time = end_break_datetime
            continue

        # Добавляем нормальный слот
        time_slots.append({
            'start_time': current_time.time(),
            'end_time': slot_end.time(),
            'date': schedule_date,
            'doctor': doctor
        })

        current_time = slot_end

    # Получаем занятые талоны для проверки конфликтов
    busy_talons = Talon.objects.filter(
        doctor=doctor,
        date=schedule_date,
        is_free=False
    )

    # Фильтруем слоты, которые не пересекаются с занятыми талонами
    available_slots = []
    for slot in time_slots:
        slot_start = datetime.combine(schedule_date, slot['start_time'])
        slot_end = datetime.combine(schedule_date, slot['end_time'])

        has_conflict = False
        for talon in busy_talons:
            talon_start = datetime.combine(talon.date, talon.start_time)
            talon_end = datetime.combine(talon.date, talon.end_time)

            # Проверяем пересечение интервалов
            if not (slot_end <= talon_start or slot_start >= talon_end):
                has_conflict = True
                break

        if not has_conflict:
            available_slots.append(slot)

    # Создаем талоны
    created_talons = []

    with transaction.atomic():
        for slot in available_slots:
            # Проверяем, нет ли уже такого талона
            existing_talon = Talon.objects.filter(
                doctor=doctor,
                date=schedule_date,
                start_time=slot['start_time'],
                end_time=slot['end_time']
            ).first()

            if not existing_talon:
                talon = Talon.objects.create(
                    doctor=doctor,
                    date=schedule_date,
                    start_time=slot['start_time'],
                    end_time=slot['end_time'],
                    is_free=True
                )
                created_talons.append(talon)

    return created_talons