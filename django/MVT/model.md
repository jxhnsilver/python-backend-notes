**Model** — это слой данных в Django, который представляет собой **Python-класс**, описывающий структуру таблицы в базе данных. Каждый экземпляр Model соответствует строке в таблице БД.
## **Для чего нужна Model?**

1. **Определение структуры БД** - Описывает таблицы, поля, связи
2. **Валидация данных** - Проверяет корректность данных перед сохранением
3. **Бизнес-логика** - Содержит методы для работы с данными
4. **Абстракция БД** - Позволяет работать с разными СУБД через единый интерфейс
5. **Миграции** - Автоматическое создание/изменение структуры БД
## **Что содержит Model?**

### 1. **Поля (Fields)** - определяют колонки таблицы
```python
class Doctor(models.Model):
    # Поле для хранения строки
    last_name = models.CharField(max_length=100)
    
    # Поле для хранения целого числа
    duration = models.IntegerField()
    
    # Поле для хранения даты
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Булево поле
    is_active = models.BooleanField(default=True)
```
### 2. **Связи (Relationships)** - определяют отношения между таблицами
```python
class Doctor(models.Model):
    # Связь один-ко-многим (один врач - одна клиника)
    clinic = models.ForeignKey(
        Clinic,  # Целевая модель
        on_delete=models.SET_NULL,  # Что делать при удалении
        null=True  # Может быть пустым
    )

class Schedule(models.Model):
    # Связь многие-ко-многим (врач может иметь много расписаний)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)

class Talon(models.Model):
    # Связь один-ко-одному
    doctor = models.OneToOneField(Doctor, on_delete=models.CASCADE)
```
### 3. **Методы (Methods)** - бизнес-логика
```python
class Doctor(models.Model):
    last_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    
    # Метод для вычисляемого поля
    @property
    def full_name(self):
        return f"{self.last_name} {self.first_name}"
    
    # Метод для строкового представления
    def __str__(self):
        return f"Doctor: {self.full_name}"
    
    # Кастомный метод
    def get_available_slots(self, date):
        """Получить свободные слоты врача на дату"""
        return Talon.objects.filter(doctor=self, date=date, is_free=True)
```
### 4. **Meta-класс** - дополнительные настройки
```python
class Doctor(models.Model):
    # Поля модели
    
    class Meta:
        # Имя таблицы в БД
        db_table = 'doctors'
        
        # Сортировка по умолчанию
        ordering = ['last_name', 'first_name']
        
        # Уникальные ограничения
        unique_together = ['last_name', 'first_name']
        
        # Человекочитаемое имя
        verbose_name = 'Врач'
        verbose_name_plural = 'Врачи'
```
## **Как используется Model?**

### 1. **CRUD операции (Create, Read, Update, Delete)**
```python
# CREATE - создание
doctor = Doctor.objects.create(
    last_name="Иванов",
    first_name="Иван",
    duration=30
)
doctor.save()

# READ - чтение
# Получить одного врача
doctor = Doctor.objects.get(id=1)

# Получить всех врачей
doctors = Doctor.objects.all()

# Фильтрация
surgeons = Doctor.objects.filter(specialization="Хирург")

# UPDATE - обновление
doctor = Doctor.objects.get(id=1)
doctor.duration = 45
doctor.save()

# Или массовое обновление
Doctor.objects.filter(clinic_id=1).update(duration=40)

# DELETE - удаление
doctor = Doctor.objects.get(id=1)
doctor.delete()

# Или массовое удаление
Doctor.objects.filter(is_active=False).delete()
```
### 2. **Сложные запросы**
```python
# Цепочки фильтров
busy_doctors = Doctor.objects.filter(
    clinic__city="Москва"
).exclude(
    is_on_vacation=True
).order_by('last_name')

# Агрегация
from django.db.models import Count, Avg

# Количество врачей в каждой клинике
stats = Clinic.objects.annotate(
    doctor_count=Count('doctor')
)

# Средняя длительность приема
avg_duration = Doctor.objects.aggregate(
    avg_duration=Avg('duration')
)

# Q-объекты для сложных условий
from django.db.models import Q

# Врачи с фамилией Иванов ИЛИ работающие в клинике 1
doctors = Doctor.objects.filter(
    Q(last_name="Иванов") | Q(clinic_id=1)
)
```
### 3. **Работа со связями**
```python
# Прямой доступ
doctor = Doctor.objects.get(id=1)
clinic = doctor.clinic  # Получить связанную клинику

# Обратный доступ (без явного ForeignKey в Clinic)
clinic = Clinic.objects.get(id=1)
doctors = clinic.doctor_set.all()  # Все врачи клиники

# Можно изменить имя обратной связи
class Doctor(models.Model):
    clinic = models.ForeignKey(
        Clinic, 
        on_delete=models.CASCADE,
        related_name='doctors'  # Теперь clinic.doctors вместо clinic.doctor_set
    )

# Тогда
clinic = Clinic.objects.get(id=1)
doctors = clinic.doctors.all()  # Все врачи клиники
```
### 4. **Валидация**
```python
class Doctor(models.Model):
    email = models.EmailField()  # Автоматическая валидация email
    
    def clean(self):
        # Кастомная валидация
        if self.duration < 10:
            raise ValidationError("Длительность приема не может быть меньше 10 минут")
    
    def save(self, *args, **kwargs):
        # Вызов валидации перед сохранением
        self.full_clean()
        super().save(*args, **kwargs)
```
## **Роль Model в проекте**

### 1. **Единый источник истины**
```python
# Везде в проекте используется одна модель
# appointments/models.py
class Schedule(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date = models.DateField()
    # ...

# appointments/views.py
def schedule_view(request):
    schedules = Schedule.objects.all()  # Используем модель

# appointments/services.py  
def create_schedule(doctor_id, date):
    schedule = Schedule.objects.create(  # Используем модель
        doctor_id=doctor_id,
        date=date
    )
```
### 2. **Безопасность данных**
```python
# Model защищает от SQL-инъекций
dangerous_input = "'; DROP TABLE doctors; --"
# Безопасно:
Doctor.objects.filter(last_name=dangerous_input)
# Запрос будет экранирован автоматически
```
### 3. **Переносимость**
```python
# Один и тот же код работает с разными БД
# settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',  # Или postgresql, mysql
    }
}

# Модели остаются неизменными
class Talon(models.Model):
    # Этот код работает с любой БД
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    start_time = models.TimeField()
```
## **Пример полной Model
```python
# appointments/models.py
from django.db import models

class Clinic(models.Model):
    """Модель клиники"""
    name = models.CharField(max_length=100)
    address = models.TextField()
    phone = models.CharField(max_length=20)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']
        verbose_name = 'Клиника'
        verbose_name_plural = 'Клиники'

class Doctor(models.Model):
    """Модель врача"""
    clinic = models.ForeignKey(
        Clinic,
        on_delete=models.SET_NULL,
        null=True,
        related_name='doctors'
    )
    last_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    patronymic = models.CharField(max_length=100)
    duration = models.IntegerField(default=30)  # длительность приема в минутах
    
    # Вычисляемое поле
    @property
    def full_name(self):
        return f"{self.last_name} {self.first_name} {self.patronymic}"
    
    def __str__(self):
        return f"Доктор {self.full_name}"
    
    # Бизнес-метод
    def is_available_on_date(self, date):
        """Проверяет, работает ли врач в указанную дату"""
        return Schedule.objects.filter(
            doctor=self,
            date=date
        ).exists()
    
    class Meta:
        ordering = ['last_name', 'first_name']
        unique_together = ['last_name', 'first_name', 'patronymic']
```
## **Преимущества использования Model**

1. **DRY (Don't Repeat Yourself)** - структура данных определяется в одном месте
2. **Безопасность** - защита от SQL-инъекций
3. **Производительность** - оптимизированные запросы через ORM
4. **Поддержка миграций** - автоматическое изменение схемы БД
5. **Админка Django** - автоматический интерфейс управления данными
6. **Тестирование** - легко создавать тестовые данные

**Model** — это основа Django-приложения, которая абстрагирует работу с БД и позволяет сосредоточиться на бизнес-логике, а не на SQL-запросах.