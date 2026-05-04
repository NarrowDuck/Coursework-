#  Електронна черга (Queue Management System)

Короткий опис проєкту: веб-додаток на FastAPI для створення та керування електронними чергами в реальному часі.

##  Функціонал
- Реєстрація та авторизація користувачів.
- Створення власних черг адміністраторами.
- Приєднання до черг та відстеження позиції.
- Автоматичне оновлення даних на сторінці.

##  Технологічний стек
- **Backend:** Python, FastAPI, SQLAlchemy
- **Database:** SQLite
- **Frontend:** Jinja2, HTML5, CSS (Pico.css), JavaScript
- **Deployment:** Railway App

## 💻 Запуск локально

1. **Клонуйте репозиторій:**
   ```bash
   git clone [https://github.com/NarrowDuck/Coursework-.git](https://github.com/NarrowDuck/Coursework-.git)
   cd Coursework-

2. **Створення віртуального оточення**
```bash
python -m venv venv
```

3. **Активація оточення**
**Для Windows:**
```bash
venv\Scripts\activate
```

4. **Встановлення залежностей**
```bash
pip install -r requirements.txt
```

5. **Запуск сервера**
```bash
uvicorn ui.main:app --reload
```

## 🔗 Посилання
- **Live Demo:** [Переглянути проєкт у хмарі](https://web-production-649d5.up.railway.app/)
