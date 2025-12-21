from django.db import models

from appointments.models.clinic import Clinic


class Doctor(models.Model):
    clinic = models.ForeignKey(
        Clinic,
        on_delete=models.SET_NULL,
        null=True
    )
    last_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    patronymic = models.CharField(max_length=100)
    full_name = models.CharField(max_length=100)
    duration = models.IntegerField()

    def __str__(self):
        return f"Doctor id: {self.id} Clinic id: {self.clinic_id} Fullname: {self.full_name} Duration: {self.duration})"
