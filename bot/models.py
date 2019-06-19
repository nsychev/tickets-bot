from config import *
from playhouse.postgres_ext import *


db = PostgresqlExtDatabase(DB_HOST, user=DB_USER, host=DB_HOST, port=DB_PORT)


class Ticket(Model):
    id = IntegerField(primary_key=True)
    name = CharField(max_length=500)
    tag = CharField(max_length=10)
    
    class Meta:
        database = db


class Image(Model):
    ticket = ForeignKeyField(Ticket)
    filename = CharField(max_length=100)
    file_id = CharField(max_length=100, null=True)
    
    class Meta:
        database = db
