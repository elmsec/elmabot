import peewee
from playhouse.db_url import connect
from elmabot import settings
from datetime import datetime


if settings.DEBUG:
    DB = peewee.SqliteDatabase(
        settings.FILE_DB_PATH, pragmas={'foreign_keys': 1})
else:
    DB = connect(settings.DATABASE_URL)


class BaseDatabaseModel(peewee.Model):
    """
        Base database model
    """
    class Meta:
        database = DB


class User(BaseDatabaseModel):
    """
        User model for the database.
        It contains all users who used the bot
    """
    telegram_id = peewee.IntegerField(unique=True)
    first_name = peewee.CharField(max_length=100)
    last_name = peewee.CharField(max_length=100, null=True)
    username = peewee.CharField(max_length=40, null=True)
    phone = peewee.CharField(max_length=40, null=True)
    bot_permission = peewee.BooleanField(default=True)
    language = peewee.CharField(max_length=10, default='tr')
    created = peewee.DateTimeField(default=datetime.now)

    def get_full_name(self):
        return (self.first_name + ' ' + (self.last_name or '')).strip()

    @classmethod
    def get_or_create_user(cls, user) -> tuple:
        return cls.get_or_create(
            telegram_id=user.id,
            defaults=dict(
                first_name=user.first_name,
                last_name=user.last_name,
                username=user.username
            ))

    @classmethod
    def register_user(cls, user):
        return cls.create(
            telegram_id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            username=user.username)

    @classmethod
    def get_user(cls, user_id):
        return cls.get_or_none(cls.telegram_id == user_id)


def initialize_db(db):
    db.connect()
    db.create_tables([User], safe=True)
    db.close()


initialize_db(DB)
