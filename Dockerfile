FROM python:alpine

RUN apk add --update --no-cache build-base postgresql-dev python3-dev musl-dev libffi-dev && \
    pip3 install python-telegram-bot peewee psycopg2 pyyaml && \
    rm -r /root/.cache && \
    apk del build-base 

ENV PYTHONPATH=/app/
WORKDIR /app/

CMD ["python3", "bot/bot.py"]
