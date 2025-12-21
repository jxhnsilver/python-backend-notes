## Основное назначение

Файл маршрутизации (URL dispatcher), который связывает URL-адреса с представлениями (views).
## Базовая структура
```python
from django.contrib import admin
from django.urls import path
from . import views  # Импорт views из текущего приложения

urlpatterns = [
    path('admin/', admin.site.urls),  # Админ-панель
    path('', views.home, name='home'),  # Главная страница
    path('about/', views.about, name='about'),
    path('articles/<int:article_id>/', views.article_detail, name='article_detail'),
]
```
## Компоненты пути (path())
```python
path(route, view, kwargs=None, name=None)
```
### 1. route (строка маршрута)
```python
# Простые маршруты
path('about/', views.about)          # /about/
path('contact-us/', views.contact)   # /contact-us/

# С параметрами
path('user/<str:username>/', views.profile)          # /user/john/
path('post/<int:year>/<int:month>/', views.archive)  # /post/2024/12/
path('page/<slug:page_slug>/', views.page)           # /page/about-us/
```
### 2. view (функция или класс)
```python
# Функциональное представление
from . import views
path('home/', views.home_function)

# Класс-представление (CBV)
from .views import HomeView
path('home-cbv/', HomeView.as_view())

# Встроенное представление
from django.views.generic import TemplateView
path('about/', TemplateView.as_view(template_name='about.html'))
```
### 3. kwargs (дополнительные аргументы)
```python
# Передача статических аргументов
path('about/', views.page, kwargs={'page_type': 'about', 'title': 'О нас'}),

# Во view.py
def page(request, page_type, title):
    # page_type='about', title='О нас'
    return render(request, 'page.html', {'title': title})
```
### 4. name (имя маршрута)
```python
# Определение с именем
path('articles/<int:id>/', views.article_detail, name='article_detail'),

# Использование в шаблонах
<a href="{% url 'article_detail' id=article.id %}">Читать</a>

# Использование в Python
from django.urls import reverse
url = reverse('article_detail', kwargs={'id': 5})  # /articles/5/

# Перенаправление
from django.shortcuts import redirect
return redirect('article_detail', id=5)
```
### Полный пример с всеми параметрами
```python
# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path(
        'article/<int:article_id>/',           # route
        views.article_view,                    # view  
        kwargs={'show_comments': True},        # kwargs
        name='article_detail'                  # name
    ),
]

# views.py
def article_view(request, article_id, show_comments):
    # article_id из URL, show_comments из kwargs
    article = get_object_or_404(Article, id=article_id)
    context = {
        'article': article,
        'show_comments': show_comments,  # Всегда True
    }
    return render(request, 'article.html', context)
```
### Важные моменты

1. **app_name** предотвращает конфликты имен между приложениями
2. **name** делает код независимым от конкретных URL
3. **kwargs** позволяет передавать статические данные в представления
4. Всегда используйте именованные URL для удобства поддержки

### Примеры
```python
# Простой путь
path('contact/', views.contact, name='contact')

# С параметром
path('user/<str:username>/', views.user_profile, name='user_profile')

# Несколько параметров
path('post/<int:year>/<int:month>/', views.post_archive, name='post_archive')
```
## Типы конвертеров параметров
| Конвертер | Пример           | Описание                  |
| --------- | ---------------- | ------------------------- |
| `str`     | `<str:slug>`     | Любая непустая строка     |
| `int`     | `<int:id>`       | Положительное целое число |
| `slug`    | `<slug:title>`   | Буквы, цифры, дефисы      |
| `uuid`    | `<uuid:uuid>`    | UUID строка               |
| `path`    | `<path:subpath>` | Любая строка с `/`        |
## Включение URL других приложений (include)
```python
from django.urls import include, path

urlpatterns = [
    path('blog/', include('blog.urls')),  # Все URL из blog/urls.py
    path('api/', include([
        path('v1/', include('api.v1.urls')),
        path('v2/', include('api.v2.urls')),
    ])),
]
```
## Файл urls.py приложения
```text
project/
├── project/
│   ├── urls.py          # Главный файл маршрутизации
│   └── ...
├── blog/
│   ├── urls.py          # Маршруты для приложения blog
│   ├── views.py
│   └── ...
└── users/
    ├── urls.py          # Маршруты для приложения users
    └── ...
```
Пример urls.py приложения:
```python
# blog/urls.py
from django.urls import path
from . import views

app_name = 'blog'  # Пространство имен

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('<int:post_id>/', views.post_detail, name='post_detail'),
    path('create/', views.post_create, name='post_create'),
]
```
## Именованные URL (name)
```python
# В urls.py
path('article/<int:id>/', views.article_view, name='article_detail')

# В шаблоне
<a href="{% url 'article_detail' id=article.id %}">Читать</a>

# В Python коде
from django.urls import reverse
url = reverse('article_detail', args=[article.id])
```
## Пространства имен (namespace)
```python
# Главный urls.py
urlpatterns = [
    path('blog/', include('blog.urls', namespace='blog')),
]

# Использование
{% url 'blog:post_detail' post.id %}
reverse('blog:post_detail', args=[post.id])
```
## Практические примеры

### CRUD маршруты
```python
# articles/urls.py
urlpatterns = [
    path('', views.ArticleListView.as_view(), name='article_list'),
    path('create/', views.ArticleCreateView.as_view(), name='article_create'),
    path('<int:pk>/', views.ArticleDetailView.as_view(), name='article_detail'),
    path('<int:pk>/update/', views.ArticleUpdateView.as_view(), name='article_update'),
    path('<int:pk>/delete/', views.ArticleDeleteView.as_view(), name='article_delete'),
]
```
### API маршруты
```python
# api/urls.py
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, PostViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'posts', PostViewSet)

urlpatterns = router.urls
```
## Основные команды и проверки
```bash
# Проверить все URL
python manage.py show_urls

# Проверить конкретный путь
python manage.py check_urls
```
## Важные правила

1. URL обрабатываются сверху вниз
2. Первое совпадение - выполнение
3. Всегда добавляйте `/` в конце (кроме корня)
4. Используйте именованные URL для удобства
5. Разделяйте маршруты по приложениям