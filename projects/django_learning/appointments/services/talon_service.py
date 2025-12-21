# appointments/services/talon_service.py
from django.db import transaction
from django.core.exceptions import ValidationError
from ..models import Talon


def book_talon(talon_id: int) -> Talon:
    """Забронировать талон"""
    try:
        with transaction.atomic():
            talon = Talon.objects.select_for_update().get(id=talon_id)

            if not talon.is_free:
                raise ValidationError(f"Талон уже забронирован")

            talon.is_free = False
            talon.save()

            return talon
    except Talon.DoesNotExist:
        raise ValueError(f"Талон с id {talon_id} не найден")


def cancel_talon(talon_id: int) -> Talon:
    """Отменить бронирование талона (сделать свободным)"""
    try:
        with transaction.atomic():
            talon = Talon.objects.select_for_update().get(id=talon_id)
            talon.is_free = True
            talon.save()
            return talon
    except Talon.DoesNotExist:
        raise ValueError(f"Талон с id {talon_id} не найден")