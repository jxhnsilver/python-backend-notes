from django.db import models

from appointments.models.clinic import Clinic
from appointments.models.doctor import Doctor


class Schedule(models.Model):
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    start_time = models.TimeField()
    end_time = models.TimeField()
    start_break_time = models.TimeField()
    end_break_time = models.TimeField()
    date = models.DateField()

    def __str__(self):
        return f"Schedule id: {self.id} Doctor id:: {self.doctor_id} Date: {self.date} Start time: {self.start_time} - End time: {self.end_time}"
