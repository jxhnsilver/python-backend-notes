`path()` — это функция Django для создания маршрутов URL. Она связывает **адрес страницы** с **функцией-обработчиком**.
###  **Синтаксис:**
```python
path(route, view, kwargs=None, name=None)
```
### **4 аргумента функции `path()`:**

#### **1. `route` (обязательный) — КУДА ведет ссылка**
Строка, которая описывает **как выглядит URL** в браузере.
```python
# 1. Статический путь (точно знаем URL)
path('about/', about_view)          # ТОЛЬКО /about/
path('contact/', contact_view)      # ТОЛЬКО /contact/

# 2. Динамический путь (не знаем точный URL заранее)
path('doctors/<int:doctor_id>/', doctor_detail_view)
# ✅ /doctors/1/   → doctor_id=1
# ✅ /doctors/5/   → doctor_id=5  
# ✅ /doctors/42/  → doctor_id=42
# ❌ /doctors/ivanov/ → ошибка (нужно int)

# 3. Разные типы данных:
path('users/<int:user_id>/', user_view)        # только числа
path('users/<str:username>/', user_view)       # любые строки
path('users/<slug:slug>/', user_view)          # URL-дружественные строки (user-profile)
path('products/<uuid:product_id>/', product_view)  # UUID
path('files/<path:file_path>/', file_view)     # пути с / (docs/report.pdf)

# 4. Несколько параметров:
path('schedule/<int:year>/<int:month>/<int:day>/', schedule_view)
# ✅ /schedule/2024/03/15/ → year=2024, month=3, day=15
```
#### **2. `view` (обязательный) — ЧТО выполнить**
Функция или класс, который **выполняет работу** когда пользователь заходит на URL.
```python
# Функция-обработчик
path('doctors/', doctors_list_view)

# Класс-обработчик (CBV)
path('doctors/', DoctorListView.as_view())
```
#### **3. `name` (опциональный) — КАК назвать (ВАЖНО!)**
Уникальное имя для URL, чтобы **ссылаться на него без хардкода**.
```python
# БЕЗ name (ПЛОХО):
<a href="/doctors/">Врачи</a>  # Если поменяем URL, придется менять ВЕЗДЕ

# С name (ХОРОШО):
<a href="{% url 'doctors_list' %}">Врачи</a>  # Автоматически подставит правильный URL
```
### **Примеры с пояснениями:**
```python
# 1. Даем имя маршруту:
path('medical/doctors/', doctors_list_view, name='doctors_list')
path('doctors/<int:id>/', doctor_detail_view, name='doctor_detail')

# 2. Используем в шаблонах:
<a href="{% url 'doctors_list' %}">Список врачей</a>
<a href="{% url 'doctor_detail' doctor.id %}">Детали врача</a>

# 3. Используем в Python-коде:
from django.shortcuts import redirect
from django.urls import reverse

# Перенаправление
return redirect('doctors_list')
return redirect('doctor_detail', doctor_id=5)

# Получение URL в коде
url = reverse('doctors_list')  # → '/doctors/'
url = reverse('doctor_detail', args=[5])  # → '/doctors/5/'

# 4. Когда меняем URL:
# БЫЛО:
path('old/doctors/', ..., name='doctors_list')

# СТАЛО:  
path('new/medical/doctors/', ..., name='doctors_list')

# ВСЕ ССЫЛКИ В {% url 'doctors_list' %} АВТОМАТИЧЕСКИ ОБНОВИЛИСЬ!
```
### **Правила именования:**
```python
# Рекомендуемые имена:
name='doctor_list'          # список
name='doctor_detail'        # детали одного
name='doctor_create'        # создание
name='doctor_update'        # обновление
name='doctor_delete'        # удаление

# Плохие имена:
name='page1'                # непонятно
name='doctors'              # может быть конфликт
name='show_doctors_page'    # слишком длинно
```
## **4. `kwargs` (keyword arguments) - "ДОПОЛНИТЕЛЬНАЯ ИНФОРМАЦИЯ"**
Словарь с **дополнительными данными**, которые передаются в view.
### **Зачем нужен:**
Когда нужно передать **статичные данные** в view, которые не зависят от URL.
```python
# 1. Простой пример:
def about_view(request, page_title, version):
    return render(request, 'about.html', {
        'title': page_title,
        'version': version
    })

path('about/', about_view, 
     kwargs={'page_title': 'О нас', 'version': '1.0'})

# При GET /about/ вызовется:
# about_view(request, page_title='О нас', version='1.0')

# 2. Параметры + kwargs:
def doctor_special_view(request, doctor_id, is_premium):
    doctor = get_doctor(doctor_id)
    return render(request, 'doctors/special.html', {
        'doctor': doctor,
        'premium': is_premium
    })

path('doctors/<int:doctor_id>/special/', doctor_special_view,
     kwargs={'is_premium': True}, name='doctor_special')

# При GET /doctors/5/special/:
# doctor_special_view(request, doctor_id=5, is_premium=True)

# 3. Конфигурация для разных версий:
path('api/v1/doctors/', api_doctor_view, 
     kwargs={'api_version': 'v1'}, name='api_v1_doctors')
path('api/v2/doctors/', api_doctor_view,
     kwargs={'api_version': 'v2'}, name='api_v2_doctors')

def api_doctor_view(request, api_version):
    if api_version == 'v1':
        return old_api_format()
    else:
        return new_api_format()
```
###  **Как работает поиск URL:**
```python
urlpatterns = [
    path('admin/', ...),           # 1
    path('doctors/special/', ...), # 2  
    path('doctors/<int:id>/', ...),# 3
    path('doctors/', ...),         # 4
]
```
**Поиск сверху вниз:**
- `GET /doctors/5/` → совпадает с #3 (`id=5`)
- `GET /doctors/special/` → совпадает с #2
- `GET /doctors/` → совпадает с #4
- `GET /admin/` → совпадает с #1

```python
# Базовый CRUD
path('', home_view, name='home'),                           # Главная
path('doctors/', doctors_list_view, name='doctors_list'),   # Список
path('doctors/<int:doctor_id>/', doctor_detail_view, name='doctor_detail'),  # Детали
path('doctors/create/', doctor_create_view, name='doctor_create'),  # Создать
path('doctors/<int:doctor_id>/edit/', doctor_edit_view, name='doctor_edit'),  # Редактировать
path('doctors/<int:doctor_id>/delete/', doctor_delete_view, name='doctor_delete'),  # Удалить

# Клиники
path('clinics/', clinics_list_view, name='clinics_list'),
path('clinics/<int:clinic_id>/doctors/', clinic_doctors_view, name='clinic_doctors'),
```
