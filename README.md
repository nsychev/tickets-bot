# Tickets Bot

Бот с билетами по матанализу (или по любому другому предмету, который вы туда закинете). 
Скидывает красивые картинки с конспектами по выбранному билету.

> **Дисклеймер**: данное программное обеспечение создано исключительно в целях *подготовки к экзаменам*.
> Автор не рекомендует использовать бота для списывания на экзамене.

Код распространяется по [лицензии MIT](LICENSE).

## Как поднять?

### Рекомендуемый способ

Поставить [Docker](https://docs.docker.com/install/) и [docker-compose](https://docs.docker.com/compose/install/).

### Также можно

Поставить [PostgreSQL](https://www.postgresql.org/download/), [Python 3](https://python.org).

Установить Python-библиотеки `PyYAML`, `python-telegram-bot`, `peewee` и `psycopg2`.

### Настройка бота

1. Скачать бота и создать необходимые директории

```bash
git clone https://github.com/nsychev/tickets-bot.git
cd tickets-bot
mkdir tickets
```

2. В `tickets/` закинуть директории с билетами.

Название директории — номер билета.

В каждом билете фотографии (скидываются по названию в алфавитном порядке) и файл `config.yml`:

```
name: Сходимость билета 1 в пространстве рациональных чисел
tag:  min
```

3. Создать бота у [@BotFather](https://t.me/BotFather) и запомнить токен.

4. Внести свои значения в `bot/config.sample.py` и переименовать его в `bot/config.py`.

5. Запустить бота.

Docker-way:
```bash
docker-compose up -d
```

Non-Docker way:
```bash
python3 bot/bot.py
```

6. Синхронизировать директорию с базой данных: от имени админа (его ID в Telegram указывается в `bot/config.py`) ввести команду `/scan`. Если изменились билеты, достаточно лишь заново просканить их ботом — перезагружать бота не нужно.

> **NB**: при (ре)старте бот **не подгружает** билеты из директории

**Готово!** Вы восхитительны!

По всем вопросам можно написать мне [в Telegram](https://t.me/nsychev)

