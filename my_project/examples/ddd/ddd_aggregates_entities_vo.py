from dataclasses import dataclass
from typing import List

# === Value Object (не имеет ID, immutable по смыслу) ===
@dataclass(frozen=True)
class FullName:
    first_name: str
    last_name: str

    def __post_init__(self):
        if not self.first_name or not self.last_name:
            raise ValueError("Имя и фамилия обязательны")

# === Entity (имеет ID и жизненный цикл) ===
class MedicalRecord:
    def __init__(self, record_id: str, diagnosis: str):
        self.id = record_id
        self.diagnosis = diagnosis

# === Aggregate Root ===
class Patient:
    """
    Агрегат 'Пациент' — корень, через который
    происходит весь доступ к внутренним сущностям.
    """
    def __init__(self, patient_id: str, name: FullName):
        self.id = patient_id
        self.name = name
        self._medical_records: List[MedicalRecord] = []

    def add_medical_record(self, record: MedicalRecord) -> None:
        # Инвариант: нельзя добавить запись с тем же ID
        if any(r.id == record.id for r in self._medical_records):
            raise ValueError("Запись с таким ID уже существует")
        self._medical_records.append(record)

    def get_diagnoses(self) -> List[str]:
        return [r.diagnosis for r in self._medical_records]

# Пример использования
if __name__ == "__main__":
    name = FullName("Иван", "Иванов")
    patient = Patient("P-1001", name)
    # record = MedicalRecord("REC-2001", "ОРВИ")
    records = [
        MedicalRecord("REC-2001", "ОРВИ"),
        MedicalRecord("REC-2002", "ГРИП")
    ]
    for record in records:
        patient.add_medical_record(record)

    print(patient.get_diagnoses())  # ['ОРВИ', 'ГРИП']