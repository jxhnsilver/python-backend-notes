## **ОПРЕДЕЛЕНИЕ**

**`prefetch_related()`** — это метод оптимизации запросов в Django ORM для работы со связями **ManyToManyField** и обратными связями (related_name). В отличие от `select_related()`, он делает **отдельные запросы** для каждой связи, но загружает все данные эффективно, избегая проблемы N+1.
## **ПРОБЛЕМА, КОТОРУЮ РЕШАЕТ prefetch_related()**

### **❌ БЕЗ prefetch_related() — ПРОБЛЕМА N+1 ДЛЯ MANYTOMANY:**
```python
# Доктор имеет ManyToMany связь со Специализациями
class Doctor(models.Model):
    specializations = models.ManyToManyField('Specialization')

# 1 запрос: получить всех врачей
doctors = Doctor.objects.all()

for doctor in doctors:  # Для 10 врачей
    for spec in doctor.specializations.all():  # 10 ДОПОЛНИТЕЛЬНЫХ запросов!
        print(spec.name)
# ИТОГО: 1 + 10 = 11 запросов к базе данных
```
### **✅ С prefetch_related() — ОПТИМИЗАЦИЯ:**
```python
# 2 запроса: врачи + все их специализации
doctors = Doctor.objects.prefetch_related('specializations').all()

for doctor in doctors:  # Для 10 врачей
    for spec in doctor.specializations.all():  # 0 дополнительных запросов!
        print(spec.name)
# ИТОГО: 2 запроса к базе данных
```
## **КАК РАБОТАЕТ prefetch_related()**

### **На уровне SQL:**
```python
# Django код
Doctor.objects.prefetch_related('specializations').filter(id__in=[1, 2, 3])
```

```sql
-- Первый запрос: врачи
SELECT id, last_name, first_name FROM doctor WHERE id IN (1, 2, 3);

-- Второй запрос: все специализации этих врачей
SELECT doctor_specialization.doctor_id, specialization.id, specialization.name
FROM specialization
INNER JOIN doctor_specialization ON specialization.id = doctor_specialization.specialization_id
WHERE doctor_specialization.doctor_id IN (1, 2, 3);
```
### **Ключевые моменты:**

1. **Делает отдельные запросы** для каждой связи
2. **Собирает ID** из первого запроса
3. **Делает второй запрос** с WHERE IN (id1, id2, id3)
4. **Связывает данные** на уровне Python (не SQL JOIN)
5. **Работает для**: ManyToManyField и обратных связей
