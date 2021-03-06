**Реализовать сервис, который принимает и отвечает на HTTP запросы.**

## Функционал

1. В случае успешной обработки сервис должен отвечать статусом 200, в случае любой ошибки — статус 400.
2. Сохранение всех объектов в базе данных.
3. Запросы:
   - `GET /city/` — получение всех городов из базы
   - `GET /city/{city_id}/street/` — получение всех улиц города
   (`city_id` — идентификатор города)
   - `POST /shop/` — создание магазина; Данный метод получает json c объектом магазина, в ответ
   возвращает id созданной записи.
   - `GET /shop/?street=&city=&open=0/1` — получение списка магазинов
     - Метод принимает параметры для фильтрации.<br> 
     Параметры не обязательны.<br> 
     В случае отсутствия параметров выводятся все магазины, если хоть один параметр есть, 
     то по нему выполняется фильтрация. 
     - **Важно!:** в объекте каждого магазина выводится название города и улицы, а не `id` записей. 
     - Параметр `open`: 0 - закрыт, 1 - открыт.<br> 
     Данный статус определяется исходя из параметров "Врем открытия", "Время закрытия"  текущего времени сервера.

## Объекты

**Магазин**:
- Название 
- Город
- Улица
- Дом
- Врем открытия
- Врем закрытия

**Город**:
- Название

**Улица**:
- Название
- Город

**Замечание: поле id у объектов не указаны, но подразумевается что они есть.<br>**
**Важно: Выстроить связи между таблицами в базе данных.**

## Инструменты
- Фреймворк для обработки http запросов `Djаngo + Djаngo Rest Frаmework`
- Реляционная БД (`PostgreSQL` - предпочтительно, `MySQL` и тд)
- Запросы в базу данных через ORM (ORM на выбор).

### Что хочется получить в результате:
- Ссылка на репозиторий, который содержит ваш проект и `README`
- Описание, как запустить ваш проект
- Подготовительные действия (установки, настройки и т.д) для успешной работы проекта 
(Информация о доступах, логины/пароли и т.д.)