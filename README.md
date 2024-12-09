# Referral System API

## Описание

Это простая реферальная система, реализованная на Django и Django REST Framework. Она позволяет пользователям регистрироваться с помощью номера телефона, активировать инвайт-коды и отслеживать пользователей, которые использовали их инвайт-коды.

## Функциональность

- Авторизация по номеру телефона.
- Имитированная отправка 4-значного кода авторизации.
- Регистрация новых пользователей в базе данных.
- Присвоение случайно сгенерированного 6-значного инвайт-кода при первой авторизации.
- Возможность ввода чужого инвайт-кода.
- Проверка существования инвайт-кода.
- Вывод списка пользователей, которые использовали инвайт-код текущего пользователя.

## Установка

1. **Клонируйте репозиторий:**

   ```bash
   git clone <URL вашего репозитория>
