# CSV_FILE_STORAGE_API

## Technologies
[![Python](https://img.shields.io/badge/-Python-464646?style=flat&logo=Python&logoColor=ffffff&color=043A6B)](https://www.python.org/)
[![Connexion](https://img.shields.io/badge/-Connexion-464646?style=flat&color=043A6B)](https://connexion.readthedocs.io/en/stable)
[![gunicorn](https://img.shields.io/badge/-gunicorn-464646?style=flat&logo=gunicorn&logoColor=ffffff&color=043A6B)](https://gunicorn.org/)
[![JWT](https://img.shields.io/badge/-JWT-464646?style=flat&color=043A6B)](https://jwt.io/)
[![Pandas](https://img.shields.io/badge/-Pandas-464646?style=flat&logo=Pandas&logoColor=ffffff&color=043A6B)](https://pandas.pydata.org/)
[![SQLAlchemy](https://img.shields.io/badge/-SQLAlchemy-464646?style=flat&color=043A6B)](https://www.sqlalchemy.org/)
[![Docker](https://img.shields.io/badge/-Docker-464646?style=flat&logo=Docker&logoColor=ffffff&color=043A6B)](https://www.docker.com/)


## Description
Мой сервис представляет собой REST API для загрузки и обработки файлов в формате CSV. Он обеспечивает возможность регистрации пользователей, аутентификации через JWT и управления загруженными файлами. Сервис позволяет пользователям загружать/удалять свои файлы CSV, просматривать список загруженных файлов с информацией о колонках и производить сортировку и фильтрацию данных в файлах.


## Functional
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

### **После запуска сервиса всю документацию по эндпоинтам можно посмотреть по адресу http://127.0.0.1:8000/api/ui**

## Examples
- **Пример запроса с фильтрацией**
  ```
  GET /api/users/files?filters=column1__eq__value1,column2__gt__value2 HTTP/1.1
  Host: 127.0.0.1:8000
  Authorization: Bearer access-token

  
  # В этом примере мы выполняем GET запрос на users/files с двумя фильтрами.
  # Фильтр column1__eq__value1 означает, что значение столбца column1 должно быть равно value1.
  # Фильтр column2__gt__value2 означает, что значение столбца column2 должно быть больше value2.
  ```
 
- **Пример запроса с сортировкой**
  ```
  GET /api/users/files?sort_columns=column1:true,column2:false HTTP/1.1
  Host: 127.0.0.1:8000
  Authorization: Bearer access-token


  # В этом примере мы выполняем GET запрос на users/files с параметром sort_columns.
  # Он указывает на несколько столбцов и их порядок сортировки.
  # column1:true означает сортировку по столбцу column1 в возрастающем порядке.
  # column2:false означает сортировку по столбцу column2 в убывающем порядке.
  ```

## How to deploy the service
1. Склонировать проект:
    ```
    git clone git@github.com:pakodev28/pro_compliance_assignment.git
    ```
    ```
    cd pro_compliance_assignment
    ```
2. Запустить проект через контейнер Docker:
    ```
    docker build -t <create image name> .
    ```
    ```
    docker run -p 8000:8000 --name <create container name> -it <image name>
    ```
3. Остановить контейнер:
    ```
    docker container stop <CONTAINER ID> or <container name>
    ```  

## TO DO
- Добавить дополнительную фильтрацию по строковы колонкам:
  - contains()
  - startswith()
  - endswith()
- Решить проблему при чтении данных и больших csv файлов.
