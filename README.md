Запуск приложения
```
uvicorn main:app --reload 
```

http://127.0.0.1:8000/docs

```
alembic init --template async alembic
alembic revision --autogenerate -m "First migration" 
alembic upgrade head
```