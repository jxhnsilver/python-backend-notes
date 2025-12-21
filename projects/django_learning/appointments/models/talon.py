from django.db import models

from appointments.models.doctor import Doctor


class Talon(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    start_time = models.TimeField()
    end_time = models.TimeField()
    date = models.DateField()
    is_free = models.BooleanField(default=True)

    def __str__(self):
        return f"Talon id: {self.id}, Doctor id: {self.doctor_id} Date: {self.date} Start time: {self.start_time} - End time: {self.end_time}"
