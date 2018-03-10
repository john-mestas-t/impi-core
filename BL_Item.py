from DB_Controlers import *
from DB import *
from datetime import datetime
import hashlib
import os
import zlib


class Utils():
    def __init__(self):
        pass

    @classmethod
    def delete_item(self, id_it):
        return DB_Item.delete_item(id_it)

    @classmethod
    def create_item(self, ls_prm):
        try:
            OB_IT = Item(ls_prm)
            OB_IT.add_item()
            return True
        except Exception:
            return False

    @classmethod
    def update_item(self, ls_prm):
        eu = ls_prm[0]  # eu = element to update
        vu = ls_prm[1]  # vu = value to update
        cu = ls_prm[2]  # cu = condicion to update
        vc = ls_prm[3]  # vc = value of condition

        try:
            if eu == 'id_oned':
                DB_Item.update_one(
                    [
                        eu,
                        vu,
                        cu,
                        vc
                    ]
                )

            elif eu == 'status_item':
                DB_Item.update_one(
                    [
                        eu,
                        vu,
                        cu,
                        vc
                    ]
                )

            elif eu == 'link_sharing':
                DB_Item.update_one(
                    [
                        eu,
                        vu,
                        cu,
                        vc
                    ]
                )
            return True
        except Exception:
            return False

    @classmethod
    def create_path(self, ls_prm):
        ph_it = ls_prm[0]  # folder path
        tp_it = ls_prm[1]  # type folder

        if tp_it == 'FILE':
            ph_it = Utils.get_parent(ph_it)

        if tp_it == 'FOLDER':
            pass

        if not os.path.exists(ph_it):
            os.makedirs(ph_it)
            return True
        else:
            return False

    @classmethod  # [old]
    def exist_folder(self, id_ac, dt_fl):
        nm_fle = Utils.normalize_path(dt_fl[1])  # item name
        ph_fle = Utils.normalize_path(dt_fl[2])  # item path

        ls_it = DB_Item.select_all_items()
        ls_it = ls_it.where(
            (Items.id_account == id_ac) &
            (Items.type_item == 'FOLDER') &
            (Items.name_item == nm_fle) &
            (Items.ph_item_ser == ph_fle)
        )

        if ls_it.exists():
            return True
        else:
            return False

    @classmethod
    def exist_file(self, dt_fl):  # [old]
        id_ac = dt_fl[0]
        nm_fle = Utils.normalize_path(dt_fl[2])  # item name
        ph_fle = Utils.normalize_path(dt_fl[3])  # item path

        ls_it = DB_Item.select('all')
        ls_it = ls_it.where(
            (Items.id_account == id_ac) &
            (Items.type_item == 'FILE') &
            (Items.name_item == nm_fle) &
            (Items.ph_item_ser == ph_fle)
        )

        if ls_it.exists():
            print('SI existe')
        else:
            print('NO NO existe')

    @classmethod
    def get_files(self, id_ac_prm, or_by=''):
        ls_it = DB_Item.select('all')
        ls_it = ls_it.where(
            (Items.id_account == id_ac_prm) &
            (Items.status_item == 'I') &
            (Items.type_item == 'FILE') &
            (Items.level_item > 0)
        )

        if or_by == 'asce':
            ls_it = ls_it.order_by(Items.level_item)

        if or_by == 'desc':
            ls_it = ls_it.order_by(Items.level_item.desc())

        return ls_it

    @classmethod
    def get_folders(self, id_ac_prm, or_by=''):
        ls_it = DB_Item.select('all')

        ls_it = ls_it.where(
            (Items.id_account == id_ac_prm) &
            (Items.status_item == 'I') &
            (Items.type_item == 'FOLDER') &
            (Items.level_item > 0)
        )

        if or_by == 'asce':
            ls_it = ls_it.order_by(Items.level_item)

        if or_by == 'desc':
            ls_it = ls_it.order_by(Items.level_item.desc())

        return ls_it

    @classmethod
    def get_father_hash(self, path):
        return Utils.get_path_to_hash(os.path.dirname(path))

    @classmethod
    def get_parent(self, p_path):
        parent_ph = os.path.abspath(os.path.join(p_path, os.pardir))
        parent_ph = Utils.normalize_path(parent_ph)

        return parent_ph

    @classmethod
    def get_path_to_hash(self, path):
        m = hashlib.md5()
        m.update(path.encode('utf-8'))
        return m.hexdigest()

    @classmethod
    def get_type(self, path):
        if os.path.isdir(path):
            return 'FOLDER'
        else:
            return 'FILE'

    @classmethod
    def get_path_item_ser(self, p_local_path, p_count_path):
        path_server = p_local_path.replace(p_count_path, '')

        if len(path_server) == 0:
            return None
        elif len(path_server) > 0:
            return path_server

    @classmethod
    def get_level_path(self, p_path):
        try:
            if p_path is not None:
                level = p_path.count('/')

            return level
        except Exception:
            return 0

    @classmethod
    def get_md5(self, path):
        hash_md5 = hashlib.md5()
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()

    @classmethod
    def get_sha1(self, path):
        sha1 = hashlib.sha1()
        try:
            file = open(os.stat.S_IREAD(path), 'rb')
            while True:
                data = file.read(4096)
                if not data:
                    break
                sha1.update(data)
        except IOError as e:
            print('File \'' + path + '\' not found!')
            print(e)
            return None
        except:
            return None
        return sha1.hexdigest

    @classmethod
    def get_crc32(self, path, block_size=1048576):
        crc = 0
        try:
            file = open(os.stat.S_IREAD(path), 'rb')
            while True:
                data = file.read(4096)
                if not data:
                    break
                crc = zlib.crc32(data, crc)
        except IOError as e:
            print('File \'' + path + '\' not found!')
            print(e)
            return None
        except:
            return None
        return str(crc).upper()

    @classmethod
    def get_name(self, path):
        return os.path.basename(path)

    @classmethod
    def get_extension(self, path):
        if self.get_type(path) == 'DIR':
            return None
        else:
            return os.path.splitext(path)[1]

    @classmethod
    def get_size(self, path):
        if self.get_type(path) == 'FILE':
            return self.get_size_file(path)
        else:
            return self.get_size_dir(path)

    @classmethod
    def get_size_file(self, path):
        return os.stat(path).st_size

    @classmethod
    def get_size_dir(self, start_path='.'):
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(start_path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                total_size += os.path.getsize(fp)
        return total_size

    @classmethod
    def combine_paths(self, ph_ac_prm, ph_it_ser_prm):
        new_ph = ph_ac_prm + '/' + ph_it_ser_prm

        return Utils.normalize_path(new_ph)

    @classmethod
    def normalize_path(self, path):
        path = os.path.normpath(path).replace("\\", "/")
        return self.delete_last_slah(path)

    @classmethod
    def delete_last_slah(self, path):
        num_path = len(path)
        if path[num_path - 1:] == '/':
            return path[:num_path - 1]
        else:
            return path

    @classmethod
    def validate_size(self, file_size):  # se pasa de 50
        top_size = 50 * 1048576

        if file_size < top_size:
            return False

        return True

    @classmethod
    def validate_extentions(self, ext_file):  # esta permitido
        # ls_ea = list_extentions_not_allowed
        ls_ea = ['.jpg', '.png', '.ini', '.exe']

        for ea in ls_ea:
            if ext_file == ea:
                return False

        return True

    @classmethod
    def create_date(self, path):
        format = '%Y-%m-%d %H:%M:%S'
        t = os.path.getctime(path)
        t = datetime.fromtimestamp(t)

        return t.strftime(format)

    @classmethod
    def modify_date(self, path):
        format = '%Y-%m-%d %H:%M:%S'
        t = os.path.getmtime(path)
        t = datetime.fromtimestamp(t)

        return t.strftime(format)

    @classmethod
    def get_id_one(self, ls_dt):
        id_on = ls_dt[0]
        ph_ac = ls_dt[1]
        ph_it = ls_dt[2]

        if id_on is not None:
            return id_on
        else:
            return 'root' if ph_ac == ph_it else None

    @classmethod
    def update_in_DB(self, ls_pr):
        return DB_Item.update_one(ls_pr)

    @classmethod
    def exist_in_DB(self, ls_pr):
        TYPE_ITEM = ls_pr[0]
        HASH_ITEM = ls_pr[1]
        HASH_PATH = ls_pr[2]
        PATH_ITEM = ls_pr[3]

        return DB_Item.exist_item([TYPE_ITEM, HASH_ITEM, HASH_PATH, PATH_ITEM])

    @classmethod
    def comply_restrictions(self, ls_pr):
        TYPE_ITEM = ls_pr[0]
        SIZE_ITEM = ls_pr[1]
        EXTN_ITEM = ls_pr[2]

        if TYPE_ITEM == 'FOLDER':
            return True

        if not Utils.validate_extentions(EXTN_ITEM):
            return False

        if Utils.validate_size(SIZE_ITEM):  # se pasa de 50???
            return False

        return True


class Item(object):
    def __init__(self, ls_dt_it):
        self.id_ac = ls_dt_it[0]
        self.ph_ac = ls_dt_it[1]
        self.st_it = ls_dt_it[2]  # st = status
        self.ph_it = ls_dt_it[3]
        self.tp_it = ls_dt_it[4]  # type item
        self.nm_it = ls_dt_it[5]  # name item
        self.ex_it = ls_dt_it[6]  # extention item
        self.sz_it = ls_dt_it[7]  # size item
        self.id_on = ls_dt_it[8]  # id onedrive

    def add_item(self):
        ID_ACCOUNT         = self.id_ac
        ID_HASH_PATH       = Utils.get_path_to_hash(self.ph_it)
        PH_ITEM_LOC        = self.ph_it
        PH_ITEM_SER        = Utils.get_path_item_ser(self.ph_it, self.ph_ac)
        LEVEL_ITEM         = Utils.get_level_path(PH_ITEM_SER)
        TYPE_ITEM          = self.tp_it
        NAME_ITEM          = self.nm_it
        EXTN_ITEM          = self.ex_it
        SIZE_ITEM          = self.sz_it
        DATE_CREATED_ITEM  = Utils.create_date(self.ph_it)
        DATE_MODIFIED_ITEM = Utils.modify_date(self.ph_it)
        HASH_MD5_ITEM      = None if TYPE_ITEM == 'FOLDER' else Utils.get_md5(self.ph_it)
        STATUS_ITEM        = 'N' if self.ph_ac == self.ph_it else self.st_it
        ID_HASH_PARENT     = Utils.get_father_hash(self.ph_it)
        ID_ONED            = Utils.get_id_one(
            [
                self.id_on,
                self.ph_ac,
                self.ph_it
            ]
        )
        LINK_SHARING = None

        d = {
            "id_account"        : ID_ACCOUNT,
            "id_hash_path"      : ID_HASH_PATH,
            "ph_item_loc"       : PH_ITEM_LOC,
            "ph_item_ser"       : PH_ITEM_SER,
            "level_item"        : LEVEL_ITEM,
            "type_item"         : TYPE_ITEM,
            "name_item"         : NAME_ITEM,
            "extn_item"         : EXTN_ITEM,
            "size_item"         : SIZE_ITEM,
            "date_created_item" : DATE_CREATED_ITEM,
            "date_modified_item": DATE_MODIFIED_ITEM,
            "hash_md5_item"     : HASH_MD5_ITEM,
            "status_item"       : STATUS_ITEM,
            "id_hash_parent"    : ID_HASH_PARENT,
            "id_oned"           : ID_ONED,
            "link_sharing"      : LINK_SHARING
        }

        try:
            DB_Item.insert_many_items([d])
            return True
        except Exception:
            return False

if __name__ == '__main__':
    pass
