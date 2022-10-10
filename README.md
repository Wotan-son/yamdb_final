![YAMDB](https://github.com/Wotan-son/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)

# Проект YaMDb
YaMDb - каталог фильмов, книг и музыкальных альбомов с системой рейтингов, отзывов и комментариев к отзывам.
### Описание проекта
Проект YaMDb представляет из себя каталог художественных произведений различных категорий. Например, произведения могут  делиться на категории ```Книги```, ```Фильмы```, ```Музыка```. Список категорий может быть расширен новыми категориями через интерфейс администратора в Django. Сами произведения в каталоге не хранятся. К произведениям из каталога пользователи могут оставлять отзывы и выставлять оценки. К отзывам пользователи могут оставлять свои комментарии.

### Проект доступен по следующим адресам:
1) http://51.250.95.74/api/v1/
2) http://51.250.95.74/admin
3) http://51.250.95.74/redoc

### ENV - необходимые переменные
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
DB_HOST=db
DB_PORT=5432
SC_KEY= Cгенерированный пароль
ALLOWED_HOSTS=django 127.0.0.1 0.0.0.0 IP_хостинга доменное_имя

### Как запустить проект:

Склонировать репозиторий
git clone https://github.com/Wotan-son/yamdb_final.git

Выполнить вход на удаленный сервер

Установить docker на сервер:
apt install docker.io 

Установить docker-compose на сервер:
DOCKER_CONFIG=${DOCKER_CONFIG:-$HOME/.docker}
mkdir -p $DOCKER_CONFIG/cli-plugins
curl -SL https://github.com/docker/compose/releases/download/v2.11.2/docker-compose-linux-x86_64 -o $DOCKER_CONFIG/cli-plugins/docker-compose
chmod +x $DOCKER_CONFIG/cli-plugins/docker-compose

Скопировать файлы docker-compose.yml и nginx.conf из директории infra на сервер:
scp docker-compose.yaml <username>@<host>:/home/<username>/docker-compose.yaml
scp -r nginx/ <username>@<host>:/home/<username>/

Для работы с Workflow добавить в Secrets:
DB_ENGINE=<django.db.backends.postgresql>
DB_NAME=<имя базы данных postgres>
DB_USER=<пользователь бд>
DB_PASSWORD=<пароль>
DB_HOST=<db>
DB_PORT=<5432>
DOCKER_PASSWORD=<пароль DockerHub>
DOCKER_USERNAME=<имя пользователя>
USER=<имя пользователя для подключения к серверу>
HOST=<адрес сервера>
PASSPHRASE=<пароль для сервера, если он установлен>
SSH_KEY=<ваш SSH ключ >

TELEGRAM_TO=<ID чата>
TELEGRAM_TOKEN=<токен вашего бота>

собрать и запустить контейнеры на сервере:
docker-compose up -d --build

После успешной сборки:
- провести миграции внутри контейнеров:
docker-compose exec web python manage.py migrate

- собрать статику проекта:
docker-compose exec web python manage.py collectstatic --no-input

- создать суперпользователя:
docker-compose exec web python manage.py createsuperuser

### Автор проекта:
 Cтудент Яндекс.Практикум - В.А. Казаков // Wotan-son

### Лицензия:
 MIT License

Copyright (c) [2022] [Kazakov Viacheslav]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.