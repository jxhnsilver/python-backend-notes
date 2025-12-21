## **ОПРЕДЕЛЕНИЕ**

**PK (Primary Key / Первичный ключ)** — это **уникальный идентификатор** каждой записи в таблице базы данных. В Django это **поле `id`**, которое автоматически создается для каждой модели, если вы явно не указали другое поле в качестве первичного ключа.
## **ЧТО ТАКОЕ PK НА ПРАКТИКЕ**

### **В вашей таблице врачей:**
```python
class Doctor(models.Model):
    # Django автоматически добавит поле:
    # id = models.AutoField(primary_key=True)
    last_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    # ...
```
### **В базе данных это выглядит так:**
```text
Таблица: appointments_doctor
┌─────┬────────────┬─────────────┬────────────┐
│ id  │ last_name  │ first_name  │ clinic_id  │  ← id = PK
├─────┼────────────┼─────────────┼────────────┤
│ 1   │ Иванов     │ Иван        │ 5          │  ← запись #1
│ 2   │ Петрова    │ Мария       │ 5          │  ← запись #2  
│ 3   │ Сидоров    │ Алексей     │ 8          │  ← запись #3
│ 4   │ Иванов     │ Сергей      │ 5          │  ← запись #4
└─────┴────────────┴─────────────┴────────────┘
```
**Ключевые свойства PK:**

1. **✅ Уникальный** — нет двух записей с одинаковым PK
2. **✅ Не NULL** — всегда имеет значение
3. **✅ Неизменяемый** — обычно не меняется после создания
4. **✅ Быстрый поиск** — индексируется автоматически

## **КАК РАБОТАЕТ PK В DJANGO**
### **Автоматическое создание:**
```python
# Вы пишете:
class Doctor(models.Model):
    last_name = models.CharField(max_length=100)
    
# Django создает:
class Doctor(models.Model):
    id = models.AutoField(primary_key=True)  # ← Автоматически!
    last_name = models.CharField(max_length=100)
```
### **Типы первичных ключей в Django:**
#### **1. AutoField (по умолчанию)**
```python
# Автоинкремент: 1, 2, 3, 4, ...
id = models.AutoField(primary_key=True)  # Django делает это за вас
```
#### **2. UUIDField (для распределенных систем)**
```python
import uuid

class Doctor(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    # Пример UUID: 123e4567-e89b-12d3-a456-426614174000
```
#### **3. Custom PK (кастомное поле)**
```python
class Clinic(models.Model):
    # Используем код клиники как PK
    code = models.CharField(
        primary_key=True,
        max_length=10,
        unique=True
    )
    name = models.CharField(max_length=100)
    
# Использование: Clinic.objects.get(code='HOSP001')
```
## **ПРАКТИЧЕСКОЕ ИСПОЛЬЗОВАНИЕ PK**

### **Пример 1: Получение объекта по PK**
```python
# Все эти способы РАБОТАЮТ ОДИНАКОВО:
doctor = Doctor.objects.get(id=5)        # Явно по id
doctor = Doctor.objects.get(pk=5)        # По primary key (pk)
doctor = Doctor.objects.get(pk=5)        # pk работает для любого поля PK!

# Если вы изменили PK на другое поле:
class Doctor(models.Model):
    doctor_id = models.CharField(primary_key=True, max_length=10)

# Теперь тоже работает:
doctor = Doctor.objects.get(pk='DOC001')  # pk указывает на doctor_id
```
### **Пример 2: В URLs и представлениях**
```python
# urls.py
path('doctors/<int:pk>/', DoctorDetailView.as_view(), name='doctor_detail')

# views.py
class DoctorDetailView(DetailView):
    model = Doctor
    # Django автоматически найдет врача по pk из URL
    
# Шаблон или код
<a href="{% url 'doctor_detail' doctor.pk %}">
    Подробнее о {{ doctor.full_name }}
</a>
```
### **Пример 3: Сравнение и фильтрация по PK**
```python
# Получить врачей с ID больше 100
doctors = Doctor.objects.filter(pk__gt=100)

# Получить конкретных врачей по их PK
doctors = Doctor.objects.filter(pk__in=[1, 5, 10, 15])

# Проверить, является ли объект PK=5
doctor = Doctor.objects.get(pk=5)
is_specific_doctor = doctor.pk == 5  # True
```
## **PK vs ID**

### **В чем разница:**

- **`id`** — это **конкретное имя поля** (обычно AutoField)
- **`pk`** — это **абстракция Django**, которая указывает на поле первичного ключа, независимо от его фактического имени
### **Пример с кастомным PK:**
```python
class Patient(models.Model):
    # Кастомный первичный ключ (не id!)
    medical_record_number = models.CharField(
        primary_key=True,
        max_length=20
    )
    name = models.CharField(max_length=100)

# Теперь:
patient = Patient.objects.get(pk='MRN20240001')  # ✅ Работает!
patient = Patient.objects.get(id='MRN20240001')  # ❌ Ошибка! Нет поля id
print(patient.pk)  # 'MRN20240001' - ссылается на medical_record_number
```
## **FK (FOREIGN KEY) СВЯЗАН С PK**
### **Как работает связь:**
```python
class Clinic(models.Model):
    id = models.AutoField(primary_key=True)  # PK клиники
    name = models.CharField(max_length=100)

class Doctor(models.Model):
    clinic = models.ForeignKey(
        Clinic, 
        on_delete=models.CASCADE,
        # В базе создастся поле clinic_id, которое ссылается на Clinic.id
    )
```
### **В базе данных:**
```text
Таблица clinics            Таблица doctors
┌─────┬────────────┐      ┌─────┬────────────┬───────────┐
│ id  │ name       │      │ id  │ last_name  │ clinic_id │
├─────┼────────────┤      ├─────┼────────────┼───────────┤
│ 5   │ Поликлиника│←─────│ 1   │ Иванов     │ 5         │
│ 8   │ Больница   │      │ 2   │ Петрова    │ 5         │
└─────┴────────────┘      │ 3   │ Сидоров    │ 8         │
                          └─────┴────────────┴───────────┘
```
## **ЛУЧШИЕ ПРАКТИКИ РАБОТЫ С PK**

### **1. Всегда используйте `pk` вместо `id` в коде**
```python
# ❌ Хрупкий код (зависит от имени поля)
doctor = Doctor.objects.get(id=5)

# ✅ Надежный код (работает с любым PK)
doctor = Doctor.objects.get(pk=5)
```
### **2. Не показывайте PK пользователям**
```python
# ❌ Плохо: PK в URL может раскрыть информацию
# /doctors/1/ - всего 1 врач в системе?
# /doctors/1001/ - уже 1000+ врачей?

# ✅ Лучше: использовать slug или UUID
path('doctors/<slug:slug>/', ...)
# или
path('doctors/<uuid:uuid>/', ...)
```
### **3. Используйте UUID для публичных API**
```python
import uuid

class Appointment(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    
# Теперь URL: /appointments/550e8400-e29b-41d4-a716-446655440000/
# Нельзя угадать другие ID
```
### **4. Не используйте бизнес-данные как PK**
```python
# ❌ Плохо: email может измениться
class User(models.Model):
    email = models.EmailField(primary_key=True)  # Опасно!

# ✅ Лучше: отдельный PK + уникальный email
class User(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)  # Уникальный, но не PK
```
