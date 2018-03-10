from DB import *
from datetime import datetime


class Controler_DB(object):
    def __init__(self):
        pass

    @classmethod
    def open_db(self):
        DB.open_db()


class DB_Item(object):
    def __init__(self):
        pass

    # ls = list
    # ph = path
    # ac = account
    @classmethod
    def update_ph_ac_sts(self, p_status):
        ls_ph_ac = []
        for c in Accounts.select():
            ls_ph_ac.append(c.path_count)

        try:
            for ph_ac in ls_ph_ac:
                q = Items.update(status=None).where(Items.path_item == ph_ac)
                q.execute()
            return True
        except Exception:
            print('Error actualizando campos root')
            return False

    @classmethod
    def insert_many_items(self, p_many_items):
        for item in p_many_items:
            a = Items(**item)
            a.save()

    @classmethod  # OLD
    def select_all_items(self):
        return Items.select()

    @classmethod
    def select(self, ty_pr='all'):
        if ty_pr == 'all':
            return Items.select()

    @classmethod
    def update_all_status(self, p_new_token):
        try:
            u = Items.update(status_item=p_new_token)
            u.execute()
        except Exception as e:
            print(e)
            print('Error al actualizar los datos a R')

    @classmethod
    def update_id_oned(self, p_id_it, p_id_oned):
        try:
            u = Items.update(oned_id=p_id_oned).where(Items.id_item == p_id_it)
            u.execute()
            return True
        except Exception as e:
            print(e)
            print('Error actualizando id_oned')
            return False

    # ls = list
    # pru = parameters to update
    @classmethod
    def update_one(self, ls_pru):
        try:
            eu = ls_pru[0]  # eu = element to update
            vu = ls_pru[1]  # vu = value to update
            cu = ls_pru[2]  # cu = condicion to update
            vc = ls_pru[3]  # vc = value of condition

            if eu == 'id_oned':
                if cu == 'id_item':
                    qu = Items.update(id_oned=vu).where(Items.id_item == vc)
                    qu.execute()

            elif eu == 'status_item':
                if cu == 'id_item':
                    qu = Items.update(status_item=vu).where(
                        Items.id_item == vc
                    )
                    qu.execute()

                if cu == 'id_hash_path':
                    qu = Items.update(status_item=vu).where(
                        Items.id_hash_path == vc
                    )
                    qu.execute()

            elif eu == 'link_sharing':
                if cu == 'id_item':
                    qu = Items.update(link_sharing=vu).where(
                        Items.id_item == vc
                    )
                    qu.execute()
            else:
                print('no fount element to update')

        except Exception as e:
            print('error: {}'.format(e))
            return False

        return True

    @classmethod
    def exist_id_hash(self, p_id_hs, p_dte_md):  # viejo [BORRAR]
        dte_md = datetime.strptime(p_dte_md, '%Y-%m-%d %H:%M:%S').date()

        try:
            # item = Items.get(Items.id_hash_fdir == p_id_hash_fdir)
            s = Items.select()
            s = s.where(
                (Items.id_hash_fdir == p_id_hs) &
                (Items.date_modified == dte_md)
            )

            if s.exists():
                return True
            else:
                return False
        except Items.DoesNotExist as e:
            print('error: {}'.format(e))

    @classmethod
    def exist_item(self, ls_pr):  # ls_pr = list_parameters
        TYPE_ITEM = ls_pr[0]
        HASH_ITEM = ls_pr[1]
        HASH_PATH = ls_pr[2]
        PATH_ITEM = ls_pr[3]

        if PATH_ITEM != "":
            ls_it = Items.select()
            ls_it = ls_it.where(
                Items.ph_item_loc == PATH_ITEM
            )

            if ls_it.exists():
                pass
            else:
                return False

        if HASH_PATH != "":
            ls_it = Items.select()
            ls_it = ls_it.where(
                Items.id_hash_path == HASH_PATH
            )

            if ls_it.exists():
                pass
            else:
                return False

        if TYPE_ITEM == "FILE":
            if not HASH_ITEM == "":
                ls_it = Items.select()
                ls_it = ls_it.where(
                    Items.hash_md5_item == HASH_ITEM
                )

                if ls_it.exists():
                    pass
                else:
                    return False

        return True

    @classmethod
    def delete_item(self, id_it_prm):
        try:
            q = Items.delete().where(
                (Items.id_item == id_it_prm) &
                (Items.status_item == 'R')
            )
            q.execute()

            return True
        except Exception:
            return False


class DB_Account(object):
    def __init__(self):
        pass

    @classmethod
    def insert_many_accounts(self, p_many_counts):
        for count in p_many_counts:
            c = Accounts(**count)
            c.save()

    @classmethod
    def select(self, tp_prm='all'):
        if tp_prm == 'all':
            return Accounts.select()


class DB_Account_sharing(object):
    def __init__(self):
        pass

    @classmethod
    def insert_many_accounts(self, ls_ac_sha):
        for ac_sha in ls_ac_sha:
            ac = Accounts_sharing(**ac_sha)
            ac.save()

    @classmethod
    def select(self, tp_prm='all'):
        if tp_prm == 'all':
            return Accounts_sharing.select()


class DB_User(object):
    def __init__(self):
        pass

    @classmethod
    def insert_many_users(self, p_many_users):
        for user in p_many_users:
            u = Users(**user)
            u.save()

    @classmethod
    def select_all_users(self):
        return Users.select()


class DB_Storage_server(object):
    def __init__(self):
        pass

    @classmethod
    def insert_one_server(self, p_one_server):
        for user in p_many_users:
            u = Users(**user)
            u.save()

    @classmethod
    def insert_many_servers(self, p_many_servers):
        for server in p_many_servers:
            s = Storage_servers(**server)
            s.save()

    @classmethod
    def select(self, ty_pr='all'):
        ls_abs = []

        if ty_pr == 'all':  # type_parameter
            return Storage_servers.select()

        if ty_pr == 'abs':
            # ls_ss = list_storage_servers
            ls_ss = Storage_servers.select()
            for ss in ls_ss:
                ls_ac = []  # ls_ac = list_accounts
                for ac in ss.accounts:
                    ls_ac.append(ac.id_account)
                ls_abs.append([ss.name_serv, ls_ac])

            return ls_abs

        if ty_pr == 'asbs':
            # ls_ss = list_storage_servers
            ls_ss = Storage_servers.select()
            for ss in ls_ss:
                ls_ac = []  # ls_ac = list_accounts
                for ac in ss.accounts_sharing:
                    ls_ac.append(ac.id_account)
                ls_abs.append([ss.name_serv, ls_ac])

            return ls_abs


if __name__ == '__main__':
    servers = [
            {
                "name_serv": "DropBox"
            }
#            ,
#            {
#                "name_serv": "OneDrive"
#            }
        ]

    users = [
                {
                    "name_user": "John",
                    "last_name": "Mestas Tejada",
                    "base_path": "C:/impi",
                    "extn_user": ".jpg/.bmp/.png/.gif/.ini/.py"
                }
            ]

    accounts_sharing = [
        {
            "id_serv" : "1",
            "path_account" : "C:/impi/jooseea@hotmail.com__dropbox__",
            "pass_serv" : "NULL",
            "email_serv" : "jooseea@hotmail.com",
            "app_name" : "godo-sync-john",
            "app_key_serv" : "2r0d52bxn9aiguz",
            "app_secret_serv" : "lsb70c3qr2farco",
            "app_access_token_serv" : "KDBpdfqzFuMAAAAAAAAEXWdGyfrKxF31nwyLk-53ilKTRJWgbcC1NsghpEmtBvPL"
        }
#        ,
#        {
#            "id_serv" : "2",
#            "path_account" : "C:/impi/yumi_roal@hotmail.com__onedrive__",
#            "pass_serv" : "NULL",
#            "email_serv" : "yumi_roal@hotmail.com",
#            "app_name" : "od_godo_app",
#            "app_key_serv" : "82f7bcee-8230-466c-b965-e50491430c7c",
#            "app_secret_serv" : "rgEOCEUdqGzcBh7jwSL96WV",
#            "app_access_token_serv" : "NULL"
#        }
    ]


    accounts = [
        {
            "id_serv" : "1",
            "path_account" : "C:/impi/juancabu@yahoo.com__dropbox__",
            "pass_serv" : "NULL",
            "email_serv" : "juancabu@yahoo.com",
            "app_name" : "impi",
            "app_key_serv" : "gb4o4cuj7zexblp",
            "app_secret_serv" : "zjn2pstcyc33xri",
            "app_access_token_serv" : "QJl9DwCmcVAAAAAAAAAACot9aTlYc3w9YZo7a7_lSOjsn8pQ0C_KYgWfE1iNs9GO"
        }
#        ,
#        {
#            "id_serv" : "2",
#            "path_account" : "C:/impi/johnet_007@hotmail.com__onedrive__",
#            "pass_serv" : "NULL",
#            "email_serv" : "johnet_007@hotmail.com",
#            "app_name" : "My Python App",
#            "app_key_serv" : "e4cbd36f-4b8f-4eaf-b35a-458c04d8454a",
#            "app_secret_serv" : "mcXDJGXG949@-pbhmwI47!*",
#            "app_access_token_serv" : "NULL"
#        }
    ]

    DB_User.insert_many_users(users)
    DB_Account.insert_many_accounts(accounts)
    DB_Account_sharing.insert_many_accounts(accounts_sharing)
    DB_Storage_server.insert_many_servers(servers)

    print("Data was loaded!")
