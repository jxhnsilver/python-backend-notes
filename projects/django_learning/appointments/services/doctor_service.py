from appointments.models import Doctor


def get_doctors() -> list[Doctor]:
    doctors = Doctor.objects.all()
    return list(doctors)


def get_doctors_by_clinic_id(clinic_id: int) -> list[Doctor]:
    doctors = Doctor.objects.filter(clinic_id=clinic_id)
    return list(doctors)


def get_doctor_by_id(doctor_id: int) -> Doctor:
    doctor = Doctor.objects.get(id=doctor_id)
    return doctor