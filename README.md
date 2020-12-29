# Блог с ветвящимися комментариями

## Запуск
* Склонировать репозиторий
* cd blog_with_threaded_comments
* python -m venv venv
* source venv/bin/activate
* pip install -r requirements.txt
* python manage.py makemigrations
* python manage.py migrate
* python manage.py runserver

## API Endpoints
| Endpoint                                         | GET                                                                    | POST  | DELETE           | PUT  |
| ------------------------------------------------ |:----------------------------------------------------------------------:|:-------------:|:-------------:| :-----:|
| /api/posts/                                      | Получить все посты                                                     | Создать пост | -- | -- |
| /api/posts/<post_id>/                            | Получить пост по post_id                                               | -- | Удалить пост | Отредактировать пост |
| /api/posts/<post_id>/comment/                    | Получить все комментариии к посту по post_id                           | Создать комментарий к посту| -- | -- |
| /api/posts/<post_id>/comment/<comment_id>/       | Получить все комментариии по comment_id к посту по post_id             | -- | Удалить комментарий | Отредактировать пост|
| /api/posts/<post_id>/comment/<comment_id>/replies| Получить все ответы к комментариию по comment_id к по посту по post_id |  Создать ответ к комментарию| --  | -- |
