# ThermoConvert 🌡

FastAPI-додаток для конвертації температур з Цельсія у Фаренгейт.

## Запуск

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

Відкрити: http://127.0.0.1:8000

## Функціонал

- Конвертація °C → °F
- Live-preview результату під час введення
- Журнал усіх конвертацій (зі зворотним порядком — найновіші вгорі)
- Очищення журналу
- REST API: `POST /api/convert`, `GET /api/history`, `DELETE /api/history`
- Довідкова таблиця відомих температурних точок

## API

```
POST /api/convert   { "celsius": 100 }  → { "celsius": 100, "fahrenheit": 212, "timestamp": "..." }
GET  /api/history                        → [...]
DELETE /api/history                      → { "message": "History cleared" }
```
