**`filter()`** — это метод QuerySet в Django ORM, который позволяет **отфильтровывать записи из базы данных по заданным условиям**. Он возвращает новый QuerySet, содержащий только те объекты, которые удовлетворяют указанным критериям.
### **Базовый синтаксис:**
```python
Model.objects.filter(поле=значение, поле__lookup=значение, ...)
```
### **Что происходит:**

1. **Вызывается** у менеджера модели (например, `Doctor.objects`)
2. **Принимает** условия фильтрации в виде именованных аргументов
3. **Возвращает** QuerySet с отфильтрованными данными
4. **Запрос в базу** выполняется только при использовании результатов
## **ТИПЫ ФИЛЬТРОВ (LOOKUPS)**

### **1. Точное совпадение (exact)**
```python
# По умолчанию
doctors = Doctor.objects.filter(last_name='Иванов')
# Эквивалентно:
doctors = Doctor.objects.filter(last_name__exact='Иванов')
```
### **2. Частичное совпадение (contains, icontains)**
```python
# Содержит строку (регистрозависимо)
doctors = Doctor.objects.filter(last_name__contains='ива')

# Содержит строку (без учета регистра) - ЧАЩЕ ВСЕГО ИСПОЛЬЗУЕТСЯ
doctors = Doctor.objects.filter(last_name__icontains='ива')
```
### **3. Начинается/заканчивается на (startswith, endswith)**
```python
# Начинается на
doctors = Doctor.objects.filter(last_name__startswith='Ив')

# Заканчивается на
doctors = Doctor.objects.filter(last_name__endswith='ов')
```
### **4. Числовые сравнения**
```python
# Больше чем
doctors = Doctor.objects.filter(duration__gt=30)      # > 30

# Больше или равно
doctors = Doctor.objects.filter(duration__gte=30)     # >= 30

# Меньше чем
doctors = Doctor.objects.filter(duration__lt=60)      # < 60

# Меньше или равно
doctors = Doctor.objects.filter(duration__lte=60)     # <= 60
```
### **5. Диапазон значений (range)**
```python
# Между 30 и 60 минут (включительно)
doctors = Doctor.objects.filter(duration__range=(30, 60))

# Между датами
from datetime import date
doctors = Doctor.objects.filter(
    hire_date__range=(date(2020, 1, 1), date(2023, 12, 31))
)
```
### **6. Вхождение в список (in)**
```python
# Длительность 15, 30 или 45 минут
doctors = Doctor.objects.filter(duration__in=[15, 30, 45])

# Врачи с определенными фамилиями
doctors = Doctor.objects.filter(last_name__in=['Иванов', 'Петров', 'Сидоров'])
```
### **7. Пустые/не пустые значения (isnull)**
```python
# Врачи без клиники
doctors_without_clinic = Doctor.objects.filter(clinic__isnull=True)

# Врачи с назначенной клиникой
doctors_with_clinic = Doctor.objects.filter(clinic__isnull=False)
```
### **Пример 1: Базовый поиск врачей**
```python
def get_doctors_by_clinic(clinic_id):
    """
    Получить всех врачей определенной клиники
    """
    return Doctor.objects.filter(
        clinic_id=clinic_id,          # точное совпадение по ID клиники
        is_active=True                # только активные врачи
    ).order_by('last_name', 'first_name')
```
### **Пример 2: Поиск по нескольким критериям**
```python
def search_doctors(search_params):
    """
    Расширенный поиск врачей с фильтрами
    """
    queryset = Doctor.objects.select_related('clinic')
    
    # Фильтр по фамилии (без учета регистра)
    if search_params.get('last_name'):
        queryset = queryset.filter(
            last_name__icontains=search_params['last_name']
        )
    
    # Фильтр по имени (без учета регистра)
    if search_params.get('first_name'):
        queryset = queryset.filter(
            first_name__icontains=search_params['first_name']
        )
    
    # Фильтр по длительности приема
    if search_params.get('min_duration'):
        queryset = queryset.filter(
            duration__gte=search_params['min_duration']
        )
    
    if search_params.get('max_duration'):
        queryset = queryset.filter(
            duration__lte=search_params['max_duration']
        )
    
    # Фильтр по клинике
    if search_params.get('clinic_id'):
        queryset = queryset.filter(
            clinic_id=search_params['clinic_id']
        )
    
    # Только активные врачи
    queryset = queryset.filter(is_active=True)
    
    # Сортировка
    sort_by = search_params.get('sort_by', 'last_name')
    if sort_by in ['last_name', 'first_name', 'duration', 'experience']:
        queryset = queryset.order_by(sort_by)
    
    return queryset
```
### **Пример 3: Фильтрация по связанным моделям**
```python
def get_doctors_with_clinic_info():
    """
    Получение врачей с фильтрацией по полям связанной модели (Clinic)
    """
    # Врачи клиник, которые активны
    doctors = Doctor.objects.filter(
        clinic__is_active=True,          # фильтр по полю Clinic
        clinic__city='Москва',           # фильтр по другому полю Clinic
        is_active=True
    ).select_related('clinic')
    
    # Врачи клиник определенного типа
    doctors = Doctor.objects.filter(
        clinic__type__in=['государственная', 'частная'],
        clinic__rating__gte=4.0
    )
    
    return doctors
```
### **Пример 4: Фильтрация с агрегацией**
```python
from django.db.models import Count, Avg

def get_clinics_with_statistics():
    """
    Получение клиник с статистикой по врачам
    """
    # Клиники, в которых больше 5 врачей
    busy_clinics = Clinic.objects.annotate(
        doctor_count=Count('doctor')
    ).filter(
        doctor_count__gt=5,
        is_active=True
    ).order_by('-doctor_count')
    
    # Клиники со средней длительностью приема > 40 минут
    clinics_with_long_appointments = Clinic.objects.annotate(
        avg_duration=Avg('doctor__duration')
    ).filter(
        avg_duration__gt=40,
        is_active=True
    ).order_by('-avg_duration')
    
    return {
        'busy_clinics': busy_clinics,
        'clinics_with_long_appointments': clinics_with_long_appointments
    }
```
### **Пример 5: Фильтрация по датам (актуально для расписаний)**
```python
from datetime import date, timedelta
from django.utils import timezone

def get_relevant_schedules():
    """
    Получение актуальных расписаний
    """
    today = timezone.now().date()
    next_week = today + timedelta(days=7)
    
    # Расписания на сегодня
    today_schedules = Schedule.objects.filter(
        date=today,
        is_active=True
    )
    
    # Расписания на текущую неделю
    week_schedules = Schedule.objects.filter(
        date__range=[today, next_week],
        is_active=True
    )
    
    # Будущие расписания (после сегодня)
    future_schedules = Schedule.objects.filter(
        date__gt=today,
        is_active=True
    ).order_by('date', 'start_time')
    
    # Расписания определенного врача на завтра
    tomorrow = today + timedelta(days=1)
    doctor_schedules = Schedule.objects.filter(
        doctor_id=5,
        date=tomorrow,
        start_time__gte='09:00',
        end_time__lte='18:00'
    )
    
    return {
        'today': today_schedules,
        'week': week_schedules,
        'future': future_schedules,
        'doctor_tomorrow': doctor_schedules
    }
```

### **Пример 6: Цепочка фильтров (Method Chaining)**
```python
# Фильтры можно объединять в цепочки
doctors = (Doctor.objects
           .filter(clinic_id=1)
           .filter(is_active=True)
           .filter(duration__gte=30)
           .exclude(last_name='Иванов')  # исключить Иванова
           .order_by('last_name'))
```
