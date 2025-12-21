from dataclasses import dataclass
from typing import List, Optional
from datetime import date

# === Value Object: идентификатор препарата ===
@dataclass(frozen=True)
class MedicationId:
    name: str
    dosage: str  # например: "500мг"

    def __post_init__(self):
        if not self.name or not self.dosage:
            raise ValueError("Название и дозировка обязательны")


# === Entity: назначение (дочерняя сущность визита) ===
class Prescription:
    """
    Сущность 'Назначение'.
    Принадлежит визиту, имеет смысл только в его контексте.
    """
    def __init__(self, medication: MedicationId, duration_days: int):
        if duration_days <= 0:
            raise ValueError("Длительность назначения > 0")
        self.medication = medication
        self.duration_days = duration_days


# === Entity: визит к врачу (дочерняя сущность агрегата Patient) ===
class MedicalVisit:
    """
    Сущность 'Визит'.
    Имеет свою идентичность (date) и коллекцию назначений.
    """
    def __init__(self, visit_date: date, doctor: str):
        self.date = visit_date
        self.doctor = doctor
        self._prescriptions: List[Prescription] = []

    def add_prescription(self, medication: MedicationId, duration_days: int) -> None:
        self._prescriptions.append(Prescription(medication, duration_days))

    def get_medications(self) -> List[str]:
        return [p.medication.name for p in self._prescriptions]


# === Aggregate Root: пациент ===
class Patient:
    """
    Агрегат 'Пациент'.
    Содержит коллекцию визитов, каждый из которых содержит назначения.
    """
    def __init__(self, patient_id: str, full_name: str):
        self.id = patient_id
        self.name = full_name
        self._visits: List[MedicalVisit] = []  # ← коллекция дочерних сущностей

    def add_visit(self, visit_date: date, doctor: str) -> None:
        """Бизнес-правило: нельзя добавить визит в будущее."""
        if visit_date > date.today():
            raise ValueError("Нельзя добавить визит в будущее")
        # Проверка уникальности по дате (пример инварианта)
        if any(v.date == visit_date for v in self._visits):
            raise ValueError("Визит на эту дату уже существует")
        self._visits.append(MedicalVisit(visit_date, doctor))

    def prescribe_medication(self, visit_date: date, medication: MedicationId, duration_days: int) -> None:
        """Добавить назначение к существующему визиту."""
        visit = self._find_visit(visit_date)
        if not visit:
            raise ValueError("Визит не найден")
        visit.add_prescription(medication, duration_days)

    def _find_visit(self, visit_date: date) -> Optional[MedicalVisit]:
        for v in self._visits:
            if v.date == visit_date:
                return v
        return None

    def get_all_medications(self) -> List[str]:
        """Плоский список всех препаратов (защита инкапсуляции)."""
        meds = []
        for visit in self._visits:
            meds.extend(visit.get_medications())
        return meds

    def get_visit_count(self) -> int:
        return len(self._visits)