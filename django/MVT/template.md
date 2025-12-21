**Template** — это файл с разметкой (обычно HTML), который содержит **статическую разметку** и **динамические конструкции** Django для подстановки данных из View.

**Простая аналогия**: Template — это **формочка для печенья**:

- Сама форма статична (HTML-разметка)
- Тесто меняется (данные из View)
- Вместе получается готовый результат
## **Для чего нужны Templates?**

### 1. **Отделение логики от представления**
```python
# View (логика)
def doctor_detail_view(request, doctor_id):
    doctor = Doctor.objects.get(id=doctor_id)
    talons = Talon.objects.filter(doctor=doctor)
    return render(request, 'doctors/detail.html', {
        'doctor': doctor,           # ← Данные
        'talons': talons,           # ← Данные  
        'page_title': 'Карточка врача'  # ← Данные
    })

# Template (представление)
<!-- doctors/detail.html -->
<h1>{{ page_title }}</h1>  <!-- ← Отображение данных -->
<p>Врач: {{ doctor.full_name }}</p>
```
### 2. **Повторное использование кода**
```html
<!-- base.html - базовый шаблон -->
<!DOCTYPE html>
<html>
<head>
    <title>{% block title %}Медицинская система{% endblock %}</title>
</head>
<body>
    {% block content %}{% endblock %}
</body>
</html>

<!-- doctors/list.html - наследует базовый -->
{% extends 'base.html' %}

{% block title %}Список врачей{% endblock %}

{% block content %}
    <h1>Список врачей</h1>
    <!-- Контент только для этой страницы -->
{% endblock %}
```
### 3. **Безопасная работа с данными**
```html
<!-- Автоматическое экранирование HTML -->
<p>Имя: {{ user_input }}</p>
<!-- Если user_input = "<script>alert('hack')</script>" -->
<!-- Выведется как текст, а не выполнится как скрипт -->

<!-- Можно отключить экранирование если нужно -->
<p>HTML: {{ html_content|safe }}</p>
```
## **Что содержит Template?**

### 1. **Переменные (Variables)** - вывод данных
```html
<!-- Простые переменные -->
<p>Врач: {{ doctor.full_name }}</p>
<p>Дата: {{ appointment.date }}</p>
<p>Статус: {{ appointment.status }}</p>

<!-- Атрибуты объектов -->
<p>Клиника: {{ doctor.clinic.name }}</p>
<p>Телефон: {{ doctor.clinic.phone }}</p>

<!-- Индексы списков/словарей -->
<p>Первый талон: {{ talons.0.start_time }}</p>
<p>Настройки: {{ settings.TIME_FORMAT }}</p>
```
### 2. **Теги (Tags)** - логика в шаблоне
```html
<!-- Условия -->
{% if talon.is_free %}
    <span style="color: green;">Свободен</span>
{% else %}
    <span style="color: red;">Занят</span>
{% endif %}

<!-- Циклы -->
<table>
    {% for doctor in doctors %}
    <tr>
        <td>{{ forloop.counter }}</td>  <!-- Номер итерации -->
        <td>{{ doctor.full_name }}</td>
        <td>{{ doctor.specialization }}</td>
    </tr>
    {% empty %}  <!-- Если список пуст -->
    <tr>
        <td colspan="3">Врачей не найдено</td>
    </tr>
    {% endfor %}
</table>

<!-- Комментарии -->
{# Это комментарий, его не увидят пользователи #}
{% comment %}
    Многострочный
    комментарий
{% endcomment %}
```
### 3. **Фильтры (Filters)** - преобразование данных
```html
<!-- Форматирование -->
<p>Дата: {{ appointment.date|date:"d.m.Y" }}</p>
<p>Время: {{ talon.start_time|time:"H:i" }}</p>  <!-- 14:30 вместо 2:30 p.m. -->
<p>Цена: {{ price|floatformat:2 }} руб.</p>      <!-- 1500.00 -->

<!-- Текст -->
<p>Имя: {{ name|title }}</p>          <!-- иван → Иван -->
<p>Описание: {{ desc|truncatechars:100 }}</p>  <!-- Обрезать до 100 символов -->
<p>Email: {{ email|lower }}</p>       <!-- Test@Mail.com → test@mail.com -->

<!-- Массивы -->
<p>Всего врачей: {{ doctors|length }}</p>
<p>Первый врач: {{ doctors|first }}</p>
<p>Последний врач: {{ doctors|last }}</p>

<!-- Значения по умолчанию -->
<p>Телефон: {{ phone|default:"не указан" }}</p>
```
### 4. **Наследование (Inheritance)**
```html
<!-- base.html - родительский шаблон -->
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>{% block title %}Медицинская система{% endblock %}</title>
    {% block extra_css %}{% endblock %}
</head>
<body>
    <header>
        <nav>
            <a href="/">Главная</a>
            <a href="/doctors/">Врачи</a>
            <a href="/schedules/">Расписания</a>
        </nav>
    </header>
    
    <main>
        {% block content %}
        <!-- Сюда подставится контент дочерних шаблонов -->
        {% endblock %}
    </main>
    
    <footer>
        {% block footer %}
        <p>© 2023 Медицинская система</p>
        {% endblock %}
    </footer>
    
    {% block extra_js %}{% endblock %}
</body>
</html>

<!-- doctors/list.html - дочерний шаблон -->
{% extends 'base.html' %}

{% block title %}Список врачей{% endblock %}

{% block extra_css %}
    <!-- Дополнительные стили только для этой страницы -->
    <style>
        .doctor-card { border: 1px solid #ccc; padding: 10px; }
    </style>
{% endblock %}

{% block content %}
    <h1>Наши врачи</h1>
    
    {% for doctor in doctors %}
    <div class="doctor-card">
        <h3>{{ doctor.full_name }}</h3>
        <p>Специализация: {{ doctor.specialization }}</p>
    </div>
    {% endfor %}
{% endblock %}
```
### 5. **Включения (Includes)**
```html
<!-- header.html -->
<header>
    <div class="logo">МедСистема</div>
    <nav>
        <a href="/doctors/">Врачи</a>
        <a href="/appointments/">Записи</a>
    </nav>
</header>

<!-- В любом шаблоне -->
{% include 'header.html' %}

<!-- С передачей контекста -->
{% include 'doctor_card.html' with doctor=current_doctor only %}

<!-- Условное включение -->
{% if user.is_authenticated %}
    {% include 'user_menu.html' %}
{% else %}
    {% include 'guest_menu.html' %}
{% endif %}
```
## **Примеры из проекта

### 1. **Шаблон списка врачей**
```html
<!-- templates/doctors/list.html -->
<!DOCTYPE html>
<html>
<head>
    <title>{{ page_title }}</title>
</head>
<body>
    <h1>{{ page_title }}</h1>
    <p>Всего врачей: {{ total_count }}</p>
    
    <table border="1">
        <tr>
            <th>ID</th>
            <th>ФИО</th>
            <th>Клиника</th>
            <th>Длительность приема</th>
            <th>Действия</th>
        </tr>
        
        {% for doctor in doctors %}
        <tr>
            <td>{{ doctor.id }}</td>
            <td>{{ doctor.full_name }}</td>
            <td>
                {% if doctor.clinic %}
                    {{ doctor.clinic.name }}
                {% else %}
                    Не указана
                {% endif %}
            </td>
            <td>{{ doctor.duration }} мин.</td>
            <td>
                <a href="{% url 'doctor_detail' doctor.id %}">Подробнее</a>
                <a href="{% url 'doctor_talons' doctor.id %}">Талоны</a>
            </td>
        </tr>
        {% empty %}
        <tr>
            <td colspan="5">Врачи не найдены</td>
        </tr>
        {% endfor %}
    </table>
    
    <div>
        <a href="/">На главную</a>
    </div>
</body>
</html>
```
### 2. **Шаблон с фильтрами**
```html
<!-- templates/talons/detail.html -->
<!DOCTYPE html>
<html>
<head>
    <title>{{ page_title }}</title>
</head>
<body>
    <h1>Талон #{{ talon.id }}</h1>
    
    <div>
        <!-- Использование фильтров для форматирования -->
        <p><strong>Врач:</strong> {{ talon.doctor.full_name|title }}</p>
        <p><strong>Дата:</strong> {{ talon.date|date:"d E Y" }}</p>  <!-- 21 декабря 2023 -->
        <p><strong>Время:</strong> {{ talon.start_time|time:"H:i" }} - {{ talon.end_time|time:"H:i" }}</p>
        
        <!-- Условный оператор -->
        <p><strong>Статус:</strong>
            {% if talon.is_free %}
                <span style="color: green;">✅ Свободен</span>
            {% else %}
                <span style="color: red;">⛔ Занят</span>
            {% endif %}
        </p>
        
        <!-- Вычисляемое значение -->
        <p><strong>Длительность:</strong> {{ talon.doctor.duration }} мин.</p>
        
        <!-- Форматирование чисел -->
        <p><strong>Стоимость:</strong> {{ talon.price|floatformat:2 }} руб.</p>
    </div>
    
    <!-- Условное отображение кнопок -->
    <div>
        {% if talon.is_free %}
            <form action="{% url 'book_talon' talon.id %}" method="post">
                {% csrf_token %}
                <button type="submit">📅 Забронировать</button>
            </form>
        {% else %}
            <p>Забронирован: {{ talon.booked_at|date:"d.m.Y H:i" }}</p>
            <form action="{% url 'cancel_talon' talon.id %}" method="post">
                {% csrf_token %}
                <button type="submit">❌ Отменить бронь</button>
            </form>
        {% endif %}
    </div>
    
    <!-- Ссылки с параметрами -->
    <p>
        <a href="{% url 'doctor_detail' talon.doctor.id %}">👨‍⚕️ Карточка врача</a> |
        <a href="{% url 'talons' %}?doctor_id={{ talon.doctor.id }}">📋 Все талоны врача</a> |
        <a href="{% url 'schedules' %}">🗓️ Расписания</a>
    </p>
</body>
</html>
```
```html

```
### 3. **Шаблон с наследованием**
```html
<!-- templates/base.html -->
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Медицинская система{% endblock %}</title>
    {% block extra_head %}{% endblock %}
</head>
<body>
    <!-- Шапка -->
    <header style="background: #f8f9fa; padding: 10px; border-bottom: 1px solid #ddd;">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <h1 style="margin: 0;">
                    <a href="/" style="text-decoration: none; color: #333;">🏥 МедСистема</a>
                </h1>
            </div>
            <nav>
                <a href="{% url 'doctors_list' %}" style="margin: 0 10px;">👨‍⚕️ Врачи</a>
                <a href="{% url 'schedules' %}" style="margin: 0 10px;">🗓️ Расписания</a>
                <a href="{% url 'talons' %}" style="margin: 0 10px;">🎫 Талоны</a>
            </nav>
        </div>
    </header>

    <!-- Контент -->
    <main style="padding: 20px;">
        <!-- Сообщения -->
        {% if messages %}
        <div style="margin-bottom: 20px;">
            {% for message in messages %}
            <div style="padding: 10px; margin: 5px 0; border-radius: 4px; 
                       {% if message.tags == 'success' %}background: #d4edda; color: #155724; border: 1px solid #c3e6cb;
                       {% elif message.tags == 'error' %}background: #f8d7da; color: #721c24; border: 1px solid #f5c6cb;
                       {% else %}background: #d1ecf1; color: #0c5460; border: 1px solid #bee5eb;{% endif %}">
                {{ message }}
            </div>
            {% endfor %}
        </div>
        {% endif %}

        {% block content %}
        <!-- Основной контент страницы -->
        {% endblock %}
    </main>

    <!-- Подвал -->
    <footer style="background: #f8f9fa; padding: 20px; border-top: 1px solid #ddd; text-align: center;">
        {% block footer %}
        <p>© {% now "Y" %} Медицинская система. Все права защищены.</p>
        <p>📞 Телефон: 8-800-123-45-67 | ✉️ Email: info@medsystem.ru</p>
        {% endblock %}
    </footer>

    {% block extra_js %}{% endblock %}
    
    <script>
        // Автоматическое скрытие сообщений через 5 секунд
        setTimeout(() => {
            const messages = document.querySelectorAll('[style*="background"]');
            messages.forEach(msg => msg.style.display = 'none');
        }, 5000);
    </script>
</body>
</html>

<!-- templates/doctors/list.html -->
{% extends 'base.html' %}

{% block title %}Список врачей | МедСистема{% endblock %}

{% block content %}
    <h1>👨‍⚕️ Наши врачи</h1>
    
    <p style="color: #666;">Всего врачей: <strong>{{ doctors|length }}</strong></p>
    
    <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 20px; margin-top: 20px;">
        {% for doctor in doctors %}
        <div style="border: 1px solid #ddd; border-radius: 8px; padding: 20px; background: white;">
            <h3 style="margin-top: 0;">{{ doctor.full_name }}</h3>
            
            <p>
                <strong>Специализация:</strong><br>
                {{ doctor.specialization|default:"Не указана" }}
            </p>
            
            <p>
                <strong>Клиника:</strong><br>
                {% if doctor.clinic %}
                    {{ doctor.clinic.name }}
                {% else %}
                    <em>Не указана</em>
                {% endif %}
            </p>
            
            <p>
                <strong>Длительность приема:</strong><br>
                {{ doctor.duration }} минут
            </p>
            
            <div style="margin-top: 15px;">
                <a href="{% url 'doctor_detail' doctor.id %}" 
                   style="display: inline-block; background: #007bff; color: white; padding: 8px 15px; 
                          text-decoration: none; border-radius: 4px; margin-right: 10px;">
                    Подробнее
                </a>
                <a href="{% url 'doctor_talons' doctor.id %}" 
                   style="display: inline-block; background: #28a745; color: white; padding: 8px 15px; 
                          text-decoration: none; border-radius: 4px;">
                    Записаться
                </a>
            </div>
        </div>
        {% empty %}
        <div style="grid-column: 1 / -1; text-align: center; padding: 40px;">
            <p style="font-size: 18px; color: #666;">😔 Врачи не найдены</p>
            <a href="{% url 'create_doctor' %}" 
               style="display: inline-block; background: #007bff; color: white; 
                      padding: 10px 20px; text-decoration: none; border-radius: 4px;">
                ➕ Добавить первого врача
            </a>
        </div>
        {% endfor %}
    </div>
{% endblock %}
```
### 4. **Шаблон формы**
```html
<!-- templates/schedules/create.html -->
{% extends 'base.html' %}

{% block title %}Создание расписания{% endblock %}

{% block content %}
    <h1>📅 Создание расписания</h1>
    
    <!-- Вывод ошибок валидации -->
    {% if form.errors %}
    <div style="background: #f8d7da; color: #721c24; padding: 10px; border-radius: 4px; margin-bottom: 20px;">
        <strong>Ошибки:</strong>
        <ul style="margin: 5px 0 0 20px;">
            {% for field, errors in form.errors.items %}
                {% for error in errors %}
                <li>{{ error }}</li>
                {% endfor %}
            {% endfor %}
        </ul>
    </div>
    {% endif %}
    
    <form method="POST" style="max-width: 500px;">
        {% csrf_token %}
        
        <div style="margin-bottom: 15px;">
            <label style="display: block; margin-bottom: 5px; font-weight: bold;">
                Врач:
            </label>
            <select name="doctor_id" required style="width: 100%; padding: 8px;">
                <option value="">Выберите врача</option>
                {% for doctor in doctors %}
                <option value="{{ doctor.id }}" 
                        {% if form.doctor_id.value == doctor.id %}selected{% endif %}>
                    {{ doctor.full_name }}
                </option>
                {% endfor %}
            </select>
        </div>
        
        <div style="margin-bottom: 15px;">
            <label style="display: block; margin-bottom: 5px; font-weight: bold;">
                Дата:
            </label>
            <input type="date" name="date" required 
                   value="{{ form.date.value|default:'' }}"
                   style="width: 100%; padding: 8px;">
        </div>
        
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 15px;">
            <div>
                <label style="display: block; margin-bottom: 5px; font-weight: bold;">
                    Начало работы:
                </label>
                <input type="time" name="start_time" required 
                       value="{{ form.start_time.value|default:'09:00' }}"
                       style="width: 100%; padding: 8px;">
            </div>
            <div>
                <label style="display: block; margin-bottom: 5px; font-weight: bold;">
                    Конец работы:
                </label>
                <input type="time" name="end_time" required 
                       value="{{ form.end_time.value|default:'18:00' }}"
                       style="width: 100%; padding: 8px;">
            </div>
        </div>
        
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 20px;">
            <div>
                <label style="display: block; margin-bottom: 5px; font-weight: bold;">
                    Начало перерыва:
                </label>
                <input type="time" name="start_break_time" required 
                       value="{{ form.start_break_time.value|default:'13:00' }}"
                       style="width: 100%; padding: 8px;">
            </div>
            <div>
                <label style="display: block; margin-bottom: 5px; font-weight: bold;">
                    Конец перерыва:
                </label>
                <input type="time" name="end_break_time" required 
                       value="{{ form.end_break_time.value|default:'14:00' }}"
                       style="width: 100%; padding: 8px;">
            </div>
        </div>
        
        <div style="display: flex; gap: 10px;">
            <button type="submit" 
                    style="background: #28a745; color: white; border: none; 
                           padding: 10px 20px; border-radius: 4px; cursor: pointer;">
                📝 Создать расписание
            </button>
            <a href="{% url 'schedules' %}" 
               style="background: #6c757d; color: white; text-decoration: none;
                      padding: 10px 20px; border-radius: 4px;">
                ← Назад
            </a>
        </div>
    </form>
{% endblock %}
```
## **Полезные теги и фильтры**

```html
<!-- Форматирование времени (ваша проблема с "noon") -->
<p>Время: {{ talon.start_time|time:"H:i" }}</p>
<!-- Результат: 09:00, 12:00, 14:30 -->

<!-- Работа с датами -->
<p>Дата: {{ schedule.date|date:"d E Y" }}</p>       <!-- 21 декабря 2023 -->
<p>Дата: {{ schedule.date|date:"d.m.Y" }}</p>       <!-- 21.12.2023 -->
<p>День недели: {{ schedule.date|date:"l" }}</p>    <!-- Thursday -->

<!-- Плаuralize для правильного склонения -->
<p>Найден {{ doctor_count }} врач{{ doctor_count|pluralize }}</p>
<!-- 1 врач, 2 врача, 5 врачей -->

<!-- Обрезание текста -->
<p>Описание: {{ doctor.description|truncatechars:100 }}</p>

<!-- Ссылки -->
<a href="{% url 'doctor_detail' doctor.id %}">{{ doctor.full_name }}</a>
<a href="{% url 'doctor_talons' doctor.id %}?date={{ today|date:'Y-m-d' }}">
    Талоны на сегодня
</a>

<!-- Математические операции (требует кастомного фильтра) -->
<p>Свободных талонов: {{ free_talons|length }} из {{ all_talons|length }}</p>
```

### **ВАЖНО ИменованниеURL**
```html
<!-- ❌ ПЛОХО: жесткие пути -->
<a href="/doctors/{{ doctor.id }}/">Подробнее</a>

<!-- ✅ ХОРОШО: именованные URL -->
<a href="{% url 'doctor_detail' doctor.id %}">Подробнее</a>

<!-- С пространством имен -->
<a href="{% url 'appointments:doctor_detail' doctor.id %}">Подробнее</a>
```

### **Проблема: 12-часовой формат времени**
```html
<!-- БЫЛО (выводит "noon"): -->
<p>Время: {{ talon.start_time }}</p>

<!-- СТАЛО (выводит "12:00"): -->
<p>Время: {{ talon.start_time|time:"H:i" }}</p>
```
### **Проблема: жесткие ссылки**
```html
<!-- БЫЛО: -->
<a href="/talons/{{ talon.id }}/free/">Освободить</a>

<!-- СТАЛО: -->
<a href="{% url 'cancel_talon' talon.id %}">Отменить бронь</a>
```

**Template** — это "лицо" вашего приложения. Хороший шаблон:

- Читаемый и поддерживаемый
- Использует наследование
- Содержит минимум логики
- Безопасно работает с данными
- Адаптивен под разные устройства (в идеале)