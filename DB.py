import os
from peewee import *


path_db = os.path.join(os.getcwd(), 'impi-database.db')


class DB(object):
    def __init__(self):
        pass

    @classmethod
    def open_db(self):
        try:
            if not Users.table_exists():
                Users.create_table(True)
        except OperationalError:
            print("Users table already exists!")

        try:
            if not Storage_servers.table_exists():
                Storage_servers.create_table(True)
        except OperationalError:
            print("Storage_servers table already exists!")

        try:
            if not Accounts_sharing.table_exists():
                Accounts_sharing.create_table(True)
        except OperationalError:
            print("Accounts_sharing table already exists!")

        try:
            if not Accounts.table_exists():
                Accounts.create_table(True)
        except OperationalError:
            print("Accounts table already exists!")

        try:
            if not Items.table_exists():
                Items.create_table(True)
        except OperationalError:
            print("Items table already exists!")


class Base_Model(Model):
    class Meta:
        database = SqliteDatabase('impi-database.db')


class Users(Base_Model):
    id_user   = IntegerField(primary_key=True, unique=True)
    name_user = TextField(null=True)
    last_name = TextField(null=True)
    base_path = TextField(null=True)
    extn_user = TextField(null=True)


class Storage_servers(Base_Model):
    id_serv   = IntegerField(primary_key=True, unique=True)
    name_serv = TextField(null=True)


class Accounts_sharing(Base_Model):
    id_account = IntegerField(primary_key=True, unique=True)
    id_serv    = ForeignKeyField(
                              Storage_servers,
                              related_name='accounts_sharing'
                              )
    path_account          = TextField(null=True)
    pass_serv             = TextField(null=True)
    email_serv            = TextField(null=True)
    app_name              = TextField(null=True)
    app_key_serv          = TextField(null=True)
    app_secret_serv       = TextField(null=True)
    app_access_token_serv = TextField(null=True)

class Accounts(Base_Model):
    id_account = IntegerField(primary_key=True, unique=True)
    id_serv    = ForeignKeyField(
                              Storage_servers,
                              related_name='accounts'
                              )
    path_account          = TextField(null=True)
    pass_serv             = TextField(null=True)
    email_serv            = TextField(null=True)
    app_name              = TextField(null=True)
    app_key_serv          = TextField(null=True)
    app_secret_serv       = TextField(null=True)
    app_access_token_serv = TextField(null=True)


class Items(Base_Model):
    id_item            = IntegerField(primary_key=True, unique=True)
    id_account         = ForeignKeyField(Accounts, related_name='items')
    id_hash_path       = TextField(null=True)
    ph_item_loc        = TextField(null=True)
    ph_item_ser        = TextField(null=True)
    level_item         = IntegerField(default=0)
    type_item          = TextField(null=True)
    name_item          = TextField(null=True)
    extn_item          = TextField(null=True)
    size_item          = IntegerField(default=0)
    date_created_item  = DateTimeField(null=True)
    date_modified_item = DateTimeField(null=True)
    hash_md5_item      = TextField(null=True)
    status_item        = TextField(null=True)
    id_hash_parent     = TextField(null=True)
    id_oned            = TextField(null=True)
    link_sharing       = TextField(null=True)


if __name__ == '__main__':
    DB.open_db()
    print("Database was created!")
