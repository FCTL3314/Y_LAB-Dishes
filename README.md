# 📃 Description

[![Python](https://img.shields.io/badge/Python-3.10-3777A7?style=flat-square)](https://www.python.org/)
[![Fastapi](https://img.shields.io/badge/FastAPI-0.100.0-009688?style=flat-square)](https://fastapi.tiangolo.com/)
[![Poetry](https://img.shields.io/badge/Poetry-1.5.1-0992E1?style=flat-square)](https://python-poetry.org/)
[![Pytest](https://img.shields.io/badge/Pytest-passed-0ca644?style=flat-square)](https://docs.pytest.org/en/7.4.x/)
[![Black](https://img.shields.io/badge/Style-Black-black?style=flat-square)](https://black.readthedocs.io/en/stable/)

#### Проект для отбора на стажировку от компании Ylab.
* #### Использовал:
  * #### Asyncpg для асинхронных запросов к базе данных.
  * #### SQLModel как обёртку поверх SQLAlchemy и Pydantic.
  * #### Alembic для миграций.
  * #### Пакетный менеджер Poetry.
* #### Выполнил все задания повышенной сложности:
  * Реализовать вывод количества подменю и блюд для Меню через один (сложный) ORM запрос.
  * Реализовать тестовый сценарий «Проверка кол-ва блюд и подменю в меню» из Postman с помощью pytest.
  * Описать API эндпоинты в соответствий c OpenAPI.
  * Реализовать в тестах аналог Django reverse() для FastAPI: Добавил каждому эндпоинту название и затем использовал его в router.url_path_for методе.
* #### Схема бд: https://dbdiagram.io/d/64b968bb02bd1c4a5e6d2e53
* #### Нет Docker Volume для бд по причине не надобности, так как для тестов бд должна быть пуста.
* #### В связи с тем, что цена блюда это строка, округление пришлось реализовать следующим образом:
```
def __init__(self, **kwargs):
    if "price" in kwargs:
        template = f"{{:.{Config.DISH_PRICE_ROUNDING}f}}"
        kwargs["price"] = template.format(float(kwargs["price"]))
    super().__init__(**kwargs)
```
* #### Анотация возвращаемых типов для сервисов реализована с помощью Generic и TypeVar, возвращаемый тип сервиса указывается при его создании в модуле dependencies.py.


# 💽 Installation

1. #### Clone or download the repository.
2. #### Fill `.env.dist` with the required variables or leave the filled ones for test start and rename the file to `.env`.
3. #### Run docker services: `docker-compose -f docker/local/docker-compose.yml up`.

> Для тестового запуска, переменные из .env.dist менять не нужно, просто переименуйте файл в .env


# ⚒️ Testing

1. #### Complete the first 2 steps of the 💽 Installation section.
2. #### Run docker services for testing: `docker-compose -f docker/local/docker-compose.yml -f docker/test/docker-compose.yml up -d`

> #### Результат выполнения тестов отображается в логах контейнера.
> Контейнер запускается, выполняет тесты и завершает свою работу. Для повторного запуска тестов необходимо перезапустить контейнер.
>
> Для того, что бы не дублировать compose файлы, команда выше использует перезапись. Первый compose файл перезаписываеться вторым.


# 🪝 Pre-Commit hooks

1. #### Install: `pre-commit install`
2. #### Run: `pre-commit run --all-files`
