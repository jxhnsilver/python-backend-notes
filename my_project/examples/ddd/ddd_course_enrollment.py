from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime

# === Value Object: идентификатор студента ===
@dataclass(frozen=True)
class StudentId:
    value: str

    def __post_init__(self):
        if not self.value or len(self.value) < 3:
            raise ValueError("ID студента должен быть не короче 3 символов")


# === Entity: зачисление (дочерняя сущность агрегата) ===
class Enrollment:
    """
    Сущность внутри агрегата Course.
    Имеет собственный жизненный цикл и идентичность (student_id).
    """
    def __init__(self, student_id: StudentId, enrolled_at: datetime):
        self.student_id = student_id
        self.enrolled_at = enrolled_at
        self._completed_at: Optional[datetime] = None

    def mark_completed(self, when: datetime) -> None:
        if when < self.enrolled_at:
            raise ValueError("Дата завершения не может быть раньше зачисления")
        self._completed_at = when

    @property
    def is_completed(self) -> bool:
        return self._completed_at is not None


# === Aggregate Root: курс ===
class Course:
    """
    Агрегат 'Курс'.
    Содержит коллекцию дочерних сущностей Enrollment.
    Все операции — через методы агрегата.
    """
    def __init__(self, course_id: str, title: str, max_students: int = 30):
        if max_students <= 0:
            raise ValueError("Макс. число студентов должно быть > 0")
        self.id = course_id
        self.title = title
        self._max_students = max_students
        self._enrollments: List[Enrollment] = []  # ← коллекция дочерних сущностей

    def enroll_student(self, student_id: str) -> None:
        """Бизнес-правило: нельзя зачислить больше max_students."""
        if self.get_enrollment_count() >= self._max_students:
            raise ValueError(f"Курс переполнен (макс. {self._max_students})")
        if self.find_enrollment(student_id):
            raise ValueError("Студент уже зачислен")
        self._enrollments.append(Enrollment(StudentId(student_id), datetime.now()))

    def complete_student(self, student_id: str) -> None:
        """Завершить курс для студента."""
        enrollment = self.find_enrollment(student_id)
        if not enrollment:
            raise ValueError("Студент не зачислен на курс")
        enrollment.mark_completed(datetime.now())

    def find_enrollment(self, student_id: str) -> Optional[Enrollment]:
        """Защищённый доступ к внутренней сущности."""
        sid = StudentId(student_id)
        for e in self._enrollments:
            if e.student_id == sid:
                return e
        return None

    def get_enrollment_count(self) -> int:
        return len(self._enrollments)

    def get_active_students(self) -> List[str]:
        """Публичный метод — возвращает копию, не оригинал!"""
        return [
            e.student_id.value
            for e in self._enrollments
            if not e.is_completed
        ]

    def get_completion_rate(self) -> float:
        """Бизнес-метрика — внутри агрегата."""
        if not self._enrollments:
            return 0.0
        completed = sum(1 for e in self._enrollments if e.is_completed)
        return completed / len(self._enrollments)