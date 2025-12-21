`request` — это **"посылка" от пользователя**, которая содержит **ВСЕ данные о запросе**.
## **Что внутри `request` (основное):**
```python
def my_view(request):
    # request содержит ВСЕ это:
    print(request.method)      # 'GET', 'POST', 'PUT', 'DELETE'
    print(request.GET)         # GET параметры (?page=2)
    print(request.POST)        # POST данные из формы
    print(request.FILES)       # Загруженные файлы
    print(request.COOKIES)     # Куки пользователя
    print(request.session)     # Данные сессии
    print(request.user)        # Информация о пользователе
    print(request.path)        # Путь URL (/doctors/)
    print(request.META)        # Вся техническая информация
```
### **1. `request.method` - КАКОЙ ТИП ЗАПРОСА**
```python
# Пример для вашего проекта:
def doctor_view(request, doctor_id):
    if request.method == 'GET':
        # Показать информацию о враче
        doctor = get_doctor_by_id(doctor_id)
        return render(request, 'doctors/detail.html', {'doctor': doctor})
    
    elif request.method == 'POST':
        # Обновить информацию о враче
        update_doctor(doctor_id, request.POST)
        return redirect('doctor_detail', doctor_id=doctor_id)
    
    elif request.method == 'DELETE':
        # Удалить врача
        delete_doctor(doctor_id)
        return JsonResponse({'status': 'deleted'})
```
**Типы методов:**
- **`GET`** - получить данные (просмотр страницы)
- **`POST`** - отправить данные (форма, создание/обновление)
- **`PUT`** - обновить данные (API)
- **`DELETE`** - удалить данные (API)
- **`PATCH`** - частичное обновление (API)
- **`HEAD`**, **`OPTIONS`** - технические
### **2. `request.GET` - ПАРАМЕТРЫ В URL (после "?")**
```python
# URL: /doctors/?page=2&search=Иванов&sort=name

def doctors_list_view(request):
    page = request.GET.get('page', '1')          # '2'
    search = request.GET.get('search', '')       # 'Иванов'
    sort = request.GET.get('sort', 'id')         # 'name'
    
    # Фильтрация врачей
    doctors = Doctor.objects.all()
    
    if search:
        doctors = doctors.filter(full_name__icontains=search)
    
    doctors = doctors.order_by(sort)
    
    # Пагинация
    paginator = Paginator(doctors, 10)
    doctors_page = paginator.get_page(int(page))
    
    return render(request, 'doctors/list.html', {
        'doctors': doctors_page,
        'search': search
    })
```
### **3. `request.POST` - ДАННЫЕ ИЗ ФОРМЫ**
```python
# Форма создания врача
def doctor_create_view(request):
    if request.method == 'GET':
        # Показать пустую форму
        return render(request, 'doctors/create.html')
    
    elif request.method == 'POST':
        # Получить данные из формы
        last_name = request.POST.get('last_name')
        first_name = request.POST.get('first_name')
        patronymic = request.POST.get('patronymic')
        duration = request.POST.get('duration')
        clinic_id = request.POST.get('clinic_id')
        
        # Создать врача
        doctor = Doctor.objects.create(
            last_name=last_name,
            first_name=first_name,
            patronymic=patronymic,
            full_name=f"{last_name} {first_name} {patronymic}",
            duration=duration,
            clinic_id=clinic_id
        )
        
        return redirect('doctor_detail', doctor_id=doctor.id)
```
### **4. `request.FILES` - ЗАГРУЖЕННЫЕ ФАЙЛЫ**
```python
# Загрузка фото врача
def upload_doctor_photo(request, doctor_id):
    if request.method == 'POST':
        photo = request.FILES.get('photo')
        
        if photo:
            # Сохранить файл
            doctor = Doctor.objects.get(id=doctor_id)
            doctor.photo = photo
            doctor.save()
            
            return redirect('doctor_detail', doctor_id=doctor_id)
    
    return render(request, 'doctors/upload_photo.html')
```
### **5. `request.user` - ИНФОРМАЦИЯ О ПОЛЬЗОВАТЕЛЕ**
```python
def doctor_profile_view(request):
    # Проверка авторизации
    if not request.user.is_authenticated:
        return redirect('login')
    
    # Кто этот пользователь?
    print(request.user.username)      # 'admin'
    print(request.user.email)         # 'admin@clinic.ru'
    print(request.user.is_staff)      # True/False
    print(request.user.is_superuser)  # True/False
    print(request.user.groups)        # Группы пользователя
    
    # Только для авторизованных
    if request.user.has_perm('appointments.view_doctor'):
        doctors = Doctor.objects.all()
    else:
        doctors = Doctor.objects.filter(is_active=True)
    
    return render(request, 'doctors/list.html', {'doctors': doctors})
```

## **КОГДА ЧТО ИСПОЛЬЗОВАТЬ:**

| Часть request         | Когда использовать         | Пример                         |
| --------------------- | -------------------------- | ------------------------------ |
| **`request.method`**  | Всегда                     | Разные действия для GET/POST   |
| **`request.GET`**     | Фильтрация, поиск          | `?page=2&search=...`           |
| **`request.POST`**    | Формы, создание/обновление | Форма создания врача           |
| **`request.FILES`**   | Загрузка файлов            | Фото врача, документы          |
| **`request.user`**    | Проверка прав              | Только админ может удалять     |
| **`request.session`** | Сохранение настроек        | Язык, тема, кол-во на странице |
| **`request.COOKIES`** | Долгосрочные данные        | Язык, авторизация              |
| **`request.META`**    | Отладка, аналитика         | IP, браузер, реферер           |