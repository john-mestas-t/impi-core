from DB_Controlers import *
from BL_Server_Engine_Utils import *
from BL_Item import *


class ServerEngine(object):
    def __init__(self, ty_server):
        self.type_server = ty_server

    def start_engine(self):
        #self.init_actio_server('download')
        self.init_actio_server('upload')
        #self.init_actio_server('delete')

    # abs = accounts by server
    # ls = list
    # ac = account
    # act = action
    # ob = object
    def init_actio_server(self, act_prm):
        ls_abs = DB_Storage_server.select('abs')

        for ls_ac in ls_abs:
            server = ls_ac[0]
            accounts = ls_ac[1]

            for ac in accounts:
                ob_ac = eval(server)(ac, self.type_server)
                ob_ac.set_act(act_prm)


class DropBox(object):
    def __init__(self, id_ac_prm, ty_server):
        # get account information with id_account
        self.type_server = ty_server
        ls_data_ac = self.get_data_ac(id_ac_prm)

        self.id_ac = ls_data_ac[0]  # id account
        self.nm_ac = ls_data_ac[1]  # name account
        self.ph_ac = ls_data_ac[2]  # path account
        self.at_ac = ls_data_ac[3]  # token

        self.ls_dt_ac = [
            self.id_ac,
            self.nm_ac,
            self.ph_ac,
            self.at_ac,
        ]

    # consult database for information about to id account
    def get_data_ac(self, id_ac_prm):
        data_ac = None
        if self.type_server == "personal":
            data_ac = DB_Account.select('all')
            data_ac = data_ac.where(Accounts.id_account == id_ac_prm)

        if self.type_server == "sharing":
            data_ac = DB_Account_sharing.select('all')
            data_ac = data_ac.where(Accounts_sharing.id_account == id_ac_prm)


        return Convert.to_list('dropbox', data_ac)

    def set_act(self, act_prm):
        if act_prm == 'upload':
            if self.type_server == "personal":
                self.up_folders()  # [OK]
                self.up_files()    # [OK]

            if self.type_server == "sharing":
                self.up_files()    # [OK]

        if act_prm == 'download':
            if self.type_server == "personal":
                self.dw_folders()  # [OK]
                self.dw_files()    # [OK]

            if self.type_server == "sharing":
                self.dw_files()    # [OK]


        if act_prm == 'delete':
            if self.type_server == "personal":
                self.dl_files()    # [OK]
                self.dl_folders()  # [OK]

            if self.type_server == "sharing":
                self.dl_files()    # [OK]

    def up_folders(self):
        ls_it = Utils.get_folders(self.id_ac)

        for it in ls_it:
            eu = 'status_item'
            vu = 'N'
            cu = 'id_item'
            vc = it.id_item

            if Utils.update_item([eu, vu, cu, vc]):
                print('UPLOADED: {} [OK]'.format(it.name_item))

    def dl_files(self):
        print("llega al up files")
        ls_it = DB_Item.select('all')
        ls_it = ls_it.where(
            (Items.id_account == self.id_ac) &
            (Items.type_item == 'FILE') &
            (Items.status_item == 'R')
        )
        print("pasa la seleccion de files")
        for it in ls_it:
            OB_DBX = SV_DropBox(self.ls_dt_ac)

            nm_it = it.name_item  # item name that will be delete

            if OB_DBX.connect():
                if OB_DBX.delete_item(it.ph_item_ser):
                    if Utils.delete_item(it.id_item):
                        print('DELETED-FILE: {} [OK]'.format(nm_it))

    def dl_folders(self):
        ls_it = DB_Item.select('all')
        ls_it = ls_it.where(
            (Items.id_account == self.id_ac) &
            (Items.type_item == 'FOLDER') &
            (Items.status_item == 'R')
        )

        ls_it = ls_it.order_by(Items.level_item.desc())

        for it in ls_it:
            OB_DBX = SV_DropBox(self.ls_dt_ac)

            nm_it = it.name_item  # item name that will be delete

            if OB_DBX.connect():
                if OB_DBX.delete_item(it.ph_item_ser):
                    if Utils.delete_item(it.id_item):
                        print('DELETED-FOLDER: {} [OK]'.format(nm_it))

    def dw_files(self):
        OB_DBX = SV_DropBox(self.ls_dt_ac)

        if OB_DBX.connect():
            for dt_fl in OB_DBX.get_files():
                nm_fle = dt_fl[0]  # nm_fl = name file
                ph_fle = Utils.normalize_path(dt_fl[1])  # Item path in server

                if not self.exist_file(nm_fle, ph_fle):
                    ph_loc = Utils.combine_paths(self.ph_ac, ph_fle)

                    Utils.create_path([ph_loc, 'FILE'])

                    df = OB_DBX.download_file(
                        [
                            ph_loc,  # path local
                            ph_fle   # path in server
                        ]
                    )

                    ci = Utils.create_item(
                        [
                            self.id_ac,
                            self.ph_ac,
                            'N',
                            ph_loc,
                            None
                        ]
                    )

                    if df:
                        print('\nDOWNLOADED-FILE: {} [OK]'.format(nm_fle))

                    if ci:
                        print('CREATED-ITEM: {} [OK]'.format(nm_fle))

    def exist_file(self, nm_it, ph_it):
        ls_it = DB_Item.select('all')
        ls_it = ls_it.where(
            (Items.id_account == self.id_ac) &
            (Items.type_item == 'FILE') &
            (Items.name_item == nm_it) &
            (Items.ph_item_ser == ph_it)
        )

        if ls_it.exists():
            return True
        else:
            return False

    def dw_folders(self):
        OB_DBX = SV_DropBox(self.ls_dt_ac)

        if OB_DBX.connect():
            OB = OB_DBX.get_folders()

            OB.sort()  # sort = sorting function
            for it in OB:
                it = it.split('|')
                ph_loc = Utils.combine_paths(self.ph_ac, it[2])
                ls_dt = [self.id_ac, self.ph_ac, 'N', ph_loc, None]

                if Utils.create_path([ph_loc, 'FOLDER']):
                    if Utils.create_item(ls_dt):
                        print('DOWNLOADED-FOLDER: {} [OK]'.format(it[1]))

    # lo = local
    # sr = server
    def up_files(self):
        ls_it = Utils.get_files(self.id_ac)
        if self.type_server == "sharing":
            ls_it = ls_it.where(
                Items.extn_item == '.properties'
            )
        else:
            ls_it = ls_it.where(
                Items.extn_item != '.properties'
            )

        # for it in Utils.get_files(self.id_ac):
        for it in ls_it:
            ov_it_lo = True  # ov = override parameter
            id_it_lo = it.id_item
            ph_it_lo = it.ph_item_loc
            ph_it_sr = it.ph_item_ser
            ph_it_sr = "/" + it.name_item if self.type_server == "sharing" else it.ph_item_ser

            OB_DBX = SV_DropBox(self.ls_dt_ac)

            if OB_DBX.connect():
                uf = OB_DBX.upload_file(
                    [
                        ov_it_lo,
                        ph_it_lo,
                        ph_it_sr
                    ]
                )

                ui = False
                if uf:
                    ui = Utils.update_item(
                        [
                            'status_item',
                            'N',
                            'id_item',
                            id_it_lo
                        ]
                    )

                us = False
                if ui:
                    sh_link = OB_DBX.get_link_sharing(ph_it_sr)
                    print("LINK-SHARED: {}".format(sh_link))
                    us = Utils.update_item(
                        [
                            'link_sharing',
                            sh_link,
                            'id_item',
                            id_it_lo
                        ]
                    )

                if uf and ui and us:
                    print('\nUPLOADED-FILE: {} [OK]'.format(it.name_item))


# nm = name
# ph = path
# ak = app_key
# as = app_secret
# dt = data
class OneDrive(object):
    def __init__(self, p_id_ac):
        # get account information with id_account
        ls_data_ac = self.get_data_ac(p_id_ac)

        self.id_ac = ls_data_ac[0]  # id
        self.nm_ac = ls_data_ac[1]  # name
        self.ph_ac = ls_data_ac[2]  # path
        self.ak_ac = ls_data_ac[3]  # key
        self.as_ac = ls_data_ac[4]  # pass

        self.ls_dt_ac = [
            self.id_ac,
            self.nm_ac,
            self.ph_ac,
            self.ak_ac,
            self.as_ac
        ]

    # consult database for information about to id account
    def get_data_ac(self, p_id_ac):
        data_ac = DB_Account.select('all')
        data_ac = data_ac.where(Accounts.id_account == p_id_ac)

        return Convert.to_list('onedrive', data_ac)

    # fld = folder
    # act = action
    def set_act(self, p_act):
        if p_act == 'upload':
            self.up_folders()  # [OK]
            self.up_files()    # [OK]

        if p_act == 'download':
            self.dw_folders()  # [OK]
            self.dw_files()    # [OK]

        if p_act == 'delete':
            self.dl_files()    # [OK]
            self.dl_folders()  # [OK]

    def dl_folders(self):
        ls_it = DB_Item.select('all')
        ls_it = ls_it.where(
            (Items.id_account == self.id_ac) &
            (Items.type_item == 'FOLDER') &
            (Items.status_item == 'R')
        )

        ls_it = ls_it.order_by(Items.level_item.desc())

        for it in ls_it:
            OB_ONE = SV_OneDrive(self.ls_dt_ac)

            nm_it = it.name_item  # item name that will be delete

            if OB_ONE.connect():
                if OB_ONE.delete_item(it.id_oned):
                    if Utils.delete_item(it.id_item):
                        print('DELETED-FOLDER: {} [OK]'.format(nm_it))
                    else:
                        print('[ERROR] borrando en DB')
                else:
                    print('[ERROR] eliminando de OD')
            else:
                print('[ERROR] conectando con OD')

    def dl_files(self):
        ls_it = DB_Item.select('all')
        ls_it = ls_it.where(
            (Items.id_account == self.id_ac) &
            (Items.type_item == 'FILE') &
            (Items.status_item == 'R')
        )

        for it in ls_it:
            OB_ONE = SV_OneDrive(self.ls_dt_ac)

            nm_it = it.name_item  # item name that will be delete

            if OB_ONE.connect():
                if OB_ONE.delete_item(it.id_oned):
                    if Utils.delete_item(it.id_item):
                        print('DELETED-FILE: {} [OK]'.format(nm_it))
                    else:
                        print('[ERROR] borrando en DB')
                else:
                    print('[ERROR] eliminando de OD')
            else:
                print('[ERROR] conectando con OD')

    def dw_folders(self):
        OB_ONED = SV_OneDrive(self.ls_dt_ac)

        if OB_ONED.connect():
            for fld in OB_ONED.get_folders():

                id_one = fld[0]  # onedrive id
                nm_one = fld[1]  # item name
                ph_one = Utils.normalize_path(fld[2])  # item path

                if not self.exist_folder(fld):

                    ph_loc = Utils.combine_paths(self.ph_ac, ph_one)

                    if Utils.create_path([ph_loc, 'FOLDER']):
                        ci = Utils.create_item(
                            [
                                self.id_ac,
                                self.ph_ac,
                                'N',
                                ph_loc,
                                id_one
                            ]
                        )

                        if ci:
                            print('DOWNLOADED-FOLDER: {} [OK]'.format(nm_one))

    def exist_folder(self, dt_fl):
        id_fld = dt_fl[1]  # id onedrive
        nm_fld = dt_fl[1]  # item name
        ph_fld = Utils.normalize_path(dt_fl[2])  # item path

        ls_it = DB_Item.select('all')
        ls_it = ls_it.where(
            (Items.id_account == self.id_ac) &
            (Items.type_item == 'FOLDER') &
            (Items.name_item == nm_fld) &
            (Items.ph_item_ser == ph_fld) &
            (Items.id_oned == id_fld)
        )

        if ls_it.exists():
            return True
        else:
            return False

    def dw_files(self):
        OB_ONED = SV_OneDrive(self.ls_dt_ac)

        if OB_ONED.connect():
            for fle in OB_ONED.get_files():

                id_one = fle[0]  # onedrive id
                nm_one = fle[1]  # item name
                ph_one = Utils.normalize_path(fle[2])  # item path

                if not self.exist_file(fle):
                    ph_loc = Utils.combine_paths(self.ph_ac, ph_one)

                    Utils.create_path([ph_loc, 'FILE'])

                    df = OB_ONED.dw_file(
                        [
                            id_one,
                            ph_loc  # ph_loc = complete local path
                        ]
                    )

                    ci = Utils.create_item(
                        [
                            self.id_ac,
                            self.ph_ac,
                            'N',
                            ph_loc,
                            id_one
                        ]
                    )

                    if df:
                        print('\nDOWNLOADED-FILE: {} [OK]'.format(nm_one))

                    if ci:
                        print('CREATED-ITEM: {} [OK]'.format(nm_one))

    def exist_file(self, dt_fle):
        id_fld = dt_fle[0]  # id onedrive
        nm_fle = dt_fle[1]  # item name
        ph_fle = Utils.normalize_path(dt_fle[2])  # item path

        ls_it = DB_Item.select('all')
        ls_it = ls_it.where(
            (Items.id_account == self.id_ac) &
            (Items.type_item == 'FILE') &
            (Items.name_item == nm_fle) &
            (Items.ph_item_ser == ph_fle) &
            (Items.id_oned == id_fld)
        )

        if ls_it.exists():
            return True
        else:
            return False

    # fle = file
    # pr = parent
    def up_files(self):
        ls_it = Utils.get_files(self.id_ac, 'asce')
        ls_it = ls_it.where(
            Items.extn_item != '.properties'
        )

        for it in ls_it:
            id_it = it.id_item
            nm_it = it.name_item
            ph_it = it.ph_item_loc
            pr_it = self.get_parent_id(ph_it)

            OB_ONED = SV_OneDrive(self.ls_dt_ac)

            if OB_ONED.connect():
                # up_item return ob item
                OB = OB_ONED.upload_file(
                    [
                        pr_it,  # pr_it = parent item
                        nm_it,  # nm_it = name item
                        ph_it   # ph_it = path item
                    ]
                )

                if OB is not None:
                    uo = Utils.update_item(
                        [
                            'id_oned',
                            OB,
                            'id_item',
                            id_it
                        ]
                    )

                    us = False
                    if uo:
                        us = Utils.update_item(
                            [
                                'status_item',
                                'N',
                                'id_item',
                                id_it
                            ]
                        )

                    usl = False
                    if us:
                        sh_link = OB_ONED.get_link_sharing(OB, 1)

                        usl = Utils.update_item(
                            [
                                'link_sharing',
                                sh_link,
                                'id_item',
                                id_it
                            ]
                        )

                    if uo and us and usl:
                        print('UPLOADED-FILE: {} [OK]'.format(nm_it))

    # ph = path
    # nm = name
    def up_folders(self):
        for i in Utils.get_folders(self.id_ac, 'asce'):
            it_fld = Utils.get_folders(self.id_ac, 'asce')

            id_fld = it_fld[0].id_item
            nm_fld = it_fld[0].name_item
            ph_fld = Utils.normalize_path(it_fld[0].ph_item_loc)
            pr_fld = self.get_parent_id(ph_fld)

            OB_ONED = SV_OneDrive(self.ls_dt_ac)

            if OB_ONED.connect():
                # up_folder = return a onedrive id
                OB = OB_ONED.upload_folder(
                    [
                        nm_fld,
                        pr_fld
                    ]
                )

                if OB is not None:
                    up = Utils.update_item(
                        [
                            'id_oned',
                            OB,
                            'id_item',
                            id_fld
                        ]
                    )

                    us = Utils.update_item(
                        [
                            'status_item',
                            'N',
                            'id_item',
                            id_fld
                        ]
                    )

                    if up and us:
                        print('UPLOADED-FOLDER: {} [OK]'.format(nm_fld))

    # it = item
    def get_parent_id(self, pt_item_prm):
        parent_ph = Utils.get_parent(pt_item_prm)

        it = DB_Item.select('all')
        it = it.where(
            (Items.id_account == self.id_ac) &
            (Items.ph_item_loc == parent_ph) &
            (~(Items.id_oned >> None))
        )

        if it.exists():
            return it[0].id_oned
        else:
            return 'root'


class GoogleDrive(object):
    def __init__(self, p_id_ac):
        pass

    def set_act(self, p_act):
        pass


if __name__ == '__main__':
    ob = ServerEngine()
    ob.start_engine()
