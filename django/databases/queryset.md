**QuerySet** — это "ленивая" (отложенная) коллекция объектов из базы данных.  
Это НЕ реальные данные, а **"обещание" получить данные**.
## **ОСНОВНЫЕ СВОЙСТВА:**

### **1. Ленивость (Lazy Evaluation)**
```python
# ЭТО НЕ ЗАПРОС К БАЗЕ!
doctors = Doctor.objects.all()  # QuerySet создан, но запрос еще НЕ выполнен

# Запрос выполнится ТОЛЬКО когда:
list(doctors)           # ← ЗДЕСЬ
for doctor in doctors:  # ← ИЛИ ЗДЕСЬ (при первой итерации)
doctors[5]              # ← ИЛИ ЗДЕСЬ
doctors.count()         # ← ИЛИ ЗДЕСЬ
```
### **2. Цепочка методов (Method Chaining)**
```python
# Можно строить цепочки без выполнения запросов
queryset = (Doctor.objects
            .filter(clinic_id=5)       # ← еще нет запроса
            .order_by('last_name')     # ← еще нет
            .exclude(is_active=False)  # ← еще нет
            .select_related('clinic')) # ← еще нет

# ВСЕ ЕЩЕ НЕТ ЗАПРОСА К БАЗЕ!
# Только ОДИН запрос выполнится в конце:
doctors = list(queryset)  # ← ЗДЕСЬ один SQL со всеми условиями
```
## **КАК СОЗДАЕТСЯ QuerySet:**

### **Из моделей (основной способ):**
```python
# Все методы managers возвращают QuerySet
Doctor.objects.all()              # QuerySet всех врачей
Doctor.objects.filter(...)        # QuerySet с фильтром
Doctor.objects.exclude(...)       # QuerySet с исключением
Clinic.objects.get(...)           # НЕ QuerySet! Один объект
```
## **МЕТОДЫ QuerySet (основные):**

### **1. Фильтрация:**
```python
# filter() - ВКЛЮЧИТЬ по условию
doctors = Doctor.objects.filter(
    clinic_id=5,                 # clinic_id равен 5
    duration__gte=30,            # duration >= 30
    last_name__startswith='И',   # фамилия начинается на И
    is_active=True               # активные врачи
)

# exclude() - ИСКЛЮЧИТЬ по условию
doctors = Doctor.objects.exclude(
    clinic_id=None,              # исключить без клиники
    duration__lt=15              # исключить < 15 минут
)

# complex lookups (сложные условия)
from django.db.models import Q
doctors = Doctor.objects.filter(
    Q(clinic_id=5) | Q(clinic_id=10),  # клиника 5 ИЛИ 10
    Q(duration__gte=30) & Q(is_active=True)  # ≥30 мин И активен
)
```
### **2. Сортировка:**
```python
# order_by() - сортировка
doctors = Doctor.objects.order_by('last_name')           # А→Я
doctors = Doctor.objects.order_by('-duration')           # по убыванию
doctors = Doctor.objects.order_by('last_name', 'first_name')  # по двум полям

# reverse() - обратный порядок
doctors = Doctor.objects.order_by('last_name').reverse()

# order_by('?') - случайный порядок (медленно!)
doctors = Doctor.objects.order_by('?')
```
### **3. Ограничение выборки:**
```python
# Срезы (как у списков)
doctors = Doctor.objects.all()[0]      # первый (не QuerySet!)
doctors = Doctor.objects.all()[:10]    # первые 10 (QuerySet)
doctors = Doctor.objects.all()[10:20]  # с 10 по 19

# Методы
doctors = Doctor.objects.all().first()    # первый
doctors = Doctor.objects.all().last()     # последний
doctor = Doctor.objects.all().get(id=5)   # конкретный (не QuerySet!)
```
### **4. Оптимизация запросов:**
```python
# select_related() - JOIN для ForeignKey (один-ко-многим)
# Врач → Клиника (у врача ОДНА клиника)
doctors = Doctor.objects.select_related('clinic')
# ОДИН запрос: SELECT doctors.*, clinics.* ...

# prefetch_related() - для обратных связей и ManyToMany
# Клиника → Врачи (у клиники МНОГО врачей)
clinics = Clinic.objects.prefetch_related('doctor_set')
# ДВА запроса: SELECT clinics.*; SELECT doctors WHERE clinic_id IN (...)

# only() / defer() - загрузить только нужные поля
doctors = Doctor.objects.only('id', 'full_name')  # только эти поля
doctors = Doctor.objects.defer('description')     # все кроме этого
```
### **5. Проверка существования:**
```python
# exists() - проверить есть ли записи
has_doctors = Doctor.objects.exists()  # True/False, быстрее чем count()>0

# contains() - проверить содержит ли QuerySet объект
doctor = Doctor.objects.get(id=5)
in_list = Doctor.objects.filter(clinic_id=1).contains(doctor)
```
