# CSV_FILE_STORAGE_API

## Description
Мой сервис представляет собой REST API для загрузки и обработки файлов в формате CSV. Он обеспечивает возможность регистрации пользователей, аутентификации через JWT и управления загруженными файлами. Сервис позволяет пользователям загружать файлы CSV, просматривать список загруженных файлов с информацией о колонках и производить сортировку и фильтрацию данных в файлах.

## Technologies
[![Python](https://img.shields.io/badge/-Python-464646?style=flat&logo=Python&logoColor=ffffff&color=043A6B)](https://www.python.org/)
[![Connexion](https://img.shields.io/badge/-Connexion-464646?style=flat&color=043A6B)](https://connexion.readthedocs.io/en/stable)
[![gunicorn](https://img.shields.io/badge/-gunicorn-464646?style=flat&logo=gunicorn&logoColor=ffffff&color=043A6B)](https://gunicorn.org/)
[![JWT](https://img.shields.io/badge/-JWT-464646?style=flat&color=043A6B)](https://jwt.io/)
[![Pandas](https://img.shields.io/badge/-Pandas-464646?style=flat&logo=Pandas&logoColor=ffffff&color=043A6B)](https://pandas.pydata.org/)
[![SQLAlchemy](https://img.shields.io/badge/-SQLAlchemy-464646?style=flat&color=043A6B)](https://www.sqlalchemy.org/)
[![Docker](https://img.shields.io/badge/-Docker-464646?style=flat&logo=Docker&logoColor=ffffff&color=043A6B)](https://www.docker.com/)


## Functional:
- Регистрация новых пользователей с защитой пароля через хеширование bcrypt.
- Аутентификация пользователей с использованием JWT.
- Загрузка файлов CSV для каждого зарегистрированного пользователя.
- Просмотр списка загруженных файлов с информацией о колонках в каждом файле.
- Возможность сортировки данных в файлах по выбранным колонкам.
- Применение фильтров к данным в файлах на основе заданных условий.
- Фильтры:
  - для колонок числового типа доступны все операторы сравнения.
  - для колонок строкового типа доступны: __eq__ и __ne__.
- Скачивание модифицированных файлов с отсортированными и отфильтрованными данными.
