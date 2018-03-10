from DB_Controlers import *
from BL_Item import *


class File_Directoy(object):
    def __init__(self, p_id_ac, p_ph_ac):
        self.id_ac = p_id_ac  #id_ac = id account
        self.ph_ac = p_ph_ac  #ph_ac = account path

        self.start_scann(self.ph_ac)

    def start_scann(self, ph_it):
        ph_it = Utils.normalize_path(ph_it)  #retorna un path limpio

        TYPE_ITEM = Utils.get_type(ph_it)
        SIZE_ITEM = Utils.get_size(ph_it)
        EXTN_ITEM = None if TYPE_ITEM == 'FOLDER' else Utils.get_extension(ph_it)
        HASH_ITEM = None if TYPE_ITEM == 'FOLDER' else Utils.get_md5(ph_it)
        HASH_PATH = Utils.get_path_to_hash(ph_it)
        PATH_ITEM = ph_it
        NAME_ITEM = Utils.get_name(ph_it)

        ls_restrictions = [
            TYPE_ITEM,  # type item
            SIZE_ITEM,  # size item
            EXTN_ITEM,  # extention item [FOLDER = NULL]
            HASH_ITEM,  # item MD5 [FOLDER = NULL]
            HASH_PATH,  # path MD5
            PATH_ITEM,  # complete item's path
            NAME_ITEM,  # only item's name, no path
        ]

        if self.exist_in_DB(ls_restrictions):
            if self.comply_restrictions(ls_restrictions):
                ob_item = Item(
                    [
                        self.id_ac,
                        self.ph_ac,
                        'I',
                        ph_it,
                        TYPE_ITEM,
                        NAME_ITEM,
                        EXTN_ITEM,
                        SIZE_ITEM,
                        None
                    ]
                )

                if ob_item.add_item():
                    print('SCANNED-ITEM: {} [OK]'.format(NAME_ITEM))

        else:
            Utils.update_in_DB(
                [
                    'status_item',
                    'N',
                    'id_hash_path',
                    HASH_PATH
                ]
            )

        if TYPE_ITEM == 'FOLDER':
            [self.start_scann(os.path.join(ph_it, x)) for x in os.listdir(ph_it)]

    def exist_in_DB(self, ls_restrictions):  # ls_pr = list_parameters
        TYPE_ITEM = ls_restrictions[0]
        SIZE_ITEM = ls_restrictions[1]
        EXTN_ITEM = ls_restrictions[2]
        HASH_ITEM = ls_restrictions[3]
        HASH_PATH = ls_restrictions[4]
        PATH_ITEM = ls_restrictions[5]
        NAME_ITEM = ls_restrictions[6]

        if not Utils.exist_in_DB([TYPE_ITEM, HASH_ITEM, HASH_PATH, PATH_ITEM]):
            return True

    def comply_restrictions(self, ls_restrictions):  # ls_pr = list_parameters
        TYPE_ITEM = ls_restrictions[0]
        SIZE_ITEM = ls_restrictions[1]
        EXTN_ITEM = ls_restrictions[2]
        HASH_ITEM = ls_restrictions[3]
        HASH_PATH = ls_restrictions[4]
        PATH_ITEM = ls_restrictions[5]
        NAME_ITEM = ls_restrictions[6]

        if Utils.comply_restrictions([TYPE_ITEM, SIZE_ITEM, EXTN_ITEM]):
            return True

        return False


if __name__ == '__main__':
    pass
