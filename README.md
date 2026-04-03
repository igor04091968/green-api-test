# GREEN-API Test Page

Статическая HTML-страница для тестового задания GREEN-API.

## Что реализовано

- `getSettings`
- `getStateInstance`
- `sendMessage`
- `sendFileByUrl`
- общий блок с `idInstance` и `ApiTokenInstance`
- read-only вывод ответа API в JSON-формате

## Локальный запуск

Достаточно открыть `index.html` в браузере.

Для запуска через простой HTTP-сервер:

```bash
cd /home/igor/green-api-test
python3 -m http.server 8080
```

После этого страница будет доступна по адресу:

`http://localhost:8080`
