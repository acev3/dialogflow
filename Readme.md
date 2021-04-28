# Бот, итеграция Dialogflow c telegram, vk.
Набор скриптов, который запускает бота(для telegram или vk группы), способного отвечать на несколько заготовленных фраз.
# Как запустить
* Для запуска сайта вам понадобится Python третьей версии.
* Скачайте код с GitHub. Затем установите зависимости
```sh
pip install -r requirements.txt
```
* Создайте файл `.env` в директории с проектом.
* Заполните `.env` следующими переменными:
```sh
CHAT_ID=chat_id
TELEGRAM_API_TOKEN=telegram_token
DEVMAN_API_TOKEN=devman_token
GOOGLE_APPLICATION_CREDENTIALS=google_credentials
PROJECT_ID=project_id
VK_GROUP_API_TOKEN=vk_token
```
chat_id - можно получить, написав боту `@userinfobot`

telegram_token - можно получить при создании бота через `@BotFather`

devman_token - в [api devman](https://dvmn.org/api/docs/)

google_credentials - создайте ключ, следуя [документации](https://cloud.google.com/docs/authentication/getting-started)

project_id - можно получить при создании [проекта](https://cloud.google.com/dialogflow/es/docs/quick/setup)

vk_token - можно узнать в настройках вк группы.

## Запустить обучение бота dialogflow
Примечание: в файле `questions.json` указан формат и данные, как пример, для обучения.
```sh
python fit_bot.py
```
## Запустить telegram бота
```sh
python telegram_bot.py
```
## Запустить vk бота
```sh
python vk_bot.py
```
## Деплой в heroku
Для того, чтобы задеплоить приложение на [heroku](https://devcenter.heroku.com/articles/getting-started-with-python), ознакомьтесь с документацией.
### Цель проекта
Код написан в образовательных целях на курсе для веб-разработчиков [dvmn.org](https://dvmn.org/modules/).