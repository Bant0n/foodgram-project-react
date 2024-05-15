# сайт - http://recipes-forall.ddns.net/
# админ - 123@aa.ru, password - 1
# Foodgram
Cервис для публикаций и обмена рецептами.

Авторизованные пользователи могут подписываться на понравившихся авторов, добавлять рецепты в избранное, в покупки, скачивать список покупок. Неавторизованным пользователям доступна регистрация, авторизация, просмотр рецептов других пользователей.

![Foodgram Workflow](https://github.com/Yan-Zhelanov/foodgram-project-react/actions/workflows/foodgram_workflow.yaml/badge.svg)


## Установка
Для запуска локально, создайте файл `.env` в директории `/backend/` с содержанием:
```
SECRET_KEY=любой_секретный_ключ_на_ваш_выбор
DEBUG=False
ALLOWED_HOSTS=*,или,ваши,хосты,через,запятые,без,пробелов
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=пароль_к_базе_данных_на_ваш_выбор
DB_HOST=bd
DB_PORT=5432
```

#### Установка Docker
Для запуска проекта вам потребуется установить Docker и docker-compose.

Для установки на ubuntu выполните следующие команды:
```bash
sudo apt install docker docker-compose
```

### Настройка проекта
1. Запустите docker compose:
```bash
docker-compose up -d
```
2. Примените миграции:
```bash
docker-compose exec backend python manage.py migrate
```
3. Заполните базу начальными данными (необязательно):
```bash
docker-compose exec backend python manange.py import_ingredients ingredieients.csv
```
4. Создайте администратора:
```bash
docker-compose exec backend python manage.py createsuperuser
```
5. Соберите статику:
```bash
docker-compose exec backend python manage.py collectstatic
```

## Как импортировать данные из своего csv файла?
Для начала убедитесь, что первая строчка вашего csv файла совпадает с названиями полей в модели. Если на первой строчке нет названия полей или они неправильные, исправьте, прежде чем приступать к импортированию.

### Импортирование с помощью скрипта
1. Заходим в shell:
```bash
docker-compose exec backend python manage.py shell
```
2. Импортируем нужные модели:
```python
from recipes.models import Ingredient, Tags
```
3. Импортируем скрипт:
```python
from scripts.import_data import create_models
```

4. Запускаем скрипт с тремя параметрами:

`file_path` — путь до вашего csv файла,

`model` — класс модели из импортированных ранее,

`print_errors` — нужно ли распечатать каждую ошибку подробно? (```True or False```)

Пример:
```python
create_models('../data/ingredients.csv', Ingredient, True)
```

## Документация к API
Чтобы открыть документацию локально, запустите сервер и перейдите по ссылке:
[http://127.0.0.1/api/docs/](http://127.0.0.1/api/docs/)
