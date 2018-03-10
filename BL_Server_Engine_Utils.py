from DB_Controlers import *
import datetime
import dropbox
import os
import sys
import stat
import time
import onedrivesdk
from onedrivesdk.helpers import GetAuthCodeServer


class Convert(object):
    def __init__(self):
        pass

    @classmethod
    def to_list(self, nm_ser_prm, dt_ac_prm):
        ls_data_ac = []

        if nm_ser_prm == 'dropbox':
            ls_data_ac.append(dt_ac_prm[0].id_account)  # 0
            ls_data_ac.append(dt_ac_prm[0].id_serv.name_serv)  # 1
            ls_data_ac.append(dt_ac_prm[0].path_account)  # 2
            ls_data_ac.append(dt_ac_prm[0].app_access_token_serv)  # 3

        if nm_ser_prm == 'onedrive':
            ls_data_ac.append(dt_ac_prm[0].id_account)  # 0
            ls_data_ac.append(dt_ac_prm[0].id_serv.name_serv)  # 1
            ls_data_ac.append(dt_ac_prm[0].path_account)  # 2
            ls_data_ac.append(dt_ac_prm[0].app_key_serv)  # 3
            ls_data_ac.append(dt_ac_prm[0].app_secret_serv)  # 4

        return ls_data_ac


class SV_DropBox(object):
    def __init__(self, p_list_dada_serv):
        self.id_ac = p_list_dada_serv[0]
        self.path_ac = p_list_dada_serv[2]
        self.token_ac = p_list_dada_serv[3]

        self.client = None

    def connect(self):
        try:
            self.client = dropbox.Dropbox(self.token_ac)
            return True
        except Exception:
            print('error connecting to the server: DropBox')
            return False

    def exist_file(self, ls_dt_it):
        nm_it_lo = ls_dt_it[0]  # nm_it_lo = file name on loca
        ph_it_lo = ls_dt_it[1]  # ph_it_lo = file path on local

        for it in self.get_files():
            nm_it_sr = it[0]
            ph_it_sr = it[1]

            if nm_it_lo == nm_it_sr and ph_it_lo == ph_it_sr:
                return True
            else:
                return False

    def delete_item(self, ph_it_prm):
        try:
            OB = self.client.files_delete(ph_it_prm)
            if OB is not None:
                return True
            else:
                return False
        except Exception:
            return False

    def download_file(self, dt_fle):
        ph_lo = dt_fle[0]  # ph_lo = local path
        ph_sr = dt_fle[1]  # ph_sr = server path

        try:
            self.client.files_download_to_file(ph_lo, ph_sr, rev=None)
            return True
        except Exception:
            return False

    # md = mode
    # ov = overwrite
    def upload_file(self, ls_dt_it):
        ov_it_lo = ls_dt_it[0]  # ov_it_lo = override mode [true/folse]
        ph_it_lo = ls_dt_it[1]  # ph_it_lo = path local
        ph_it_sr = ls_dt_it[2]  # ph_it_sr = path server

        mode = (dropbox.files.WriteMode.overwrite
                if ov_it_lo else dropbox.files.WriteMode.add)

        with open(ph_it_lo, 'rb') as f:
            data = f.read()
            try:
                res = self.client.files_upload(
                    data, ph_it_sr, mode,
                    client_modified=self.get_mtime(ph_it_lo),
                    mute=True)

                return False if res is None else True
            except dropbox.exceptions.ApiError:
                return False

    def get_mtime(self, p_path):
        mtime = os.path.getmtime(p_path)
        print(mtime)
        return datetime.datetime(*time.gmtime(mtime)[:6])

    # fl = file
    def get_files(self):
        ls_fl = []
        dt_fl = []

        for it in self.client.files_list_folder('', recursive=True).entries:
            try:
                it.client_modified
                dt_fl = [it.name, it.path_display]

                ls_fl.append(dt_fl)
            except Exception:
                pass

        return ls_fl

    def get_folders(self):
        ls_flr = []

        for it in self.client.files_list_folder('', recursive=True).entries:

            subs = str(it)
            if 'FolderMetadata' in subs:
                lv_it = it.path_display.count('/')
                nm_it = it.name
                ph_it = it.path_display
                ls_flr.append(str(lv_it) + '|' + nm_it + '|' + ph_it)

        return ls_flr

    def get_link_sharing(self, path_it):
        try:
            print('Path-Sharing: {}'.format(path_it))
            return self.client.sharing_create_shared_link(path_it, True).url
        except Exception as e:
            print(e)
            return None


class SV_OneDrive(object):
    def __init__(self, p_list_dada_serv):
        self.number_ups = []

        self.id_ac = p_list_dada_serv[0]
        self.path_ac = p_list_dada_serv[2]
        self.app_key_ac = p_list_dada_serv[3]
        self.app_secret_ac = p_list_dada_serv[4]

        self.client = None

    def connect(self):
        try:
            redirect_uri = "http://localhost:8080/"
            client_id = self.app_key_ac
            client_secret = self.app_secret_ac
            self.client = onedrivesdk.get_default_client(client_id=client_id,
                                                scopes=['wl.signin',
                                                        'wl.offline_access',
                                                        'onedrive.readwrite'])
            auth_url = self.client.auth_provider.get_auth_url(redirect_uri)

            code = GetAuthCodeServer.get_auth_code(auth_url, redirect_uri)
            self.client.auth_provider.authenticate(code, redirect_uri, client_secret)
            return True
        except Exception:
            print('error connecting to the server: OneDive')
            return False

    def upload_folder(self, ls_dt_fld):
        nm_fld = ls_dt_fld[0]  # nm_fld = name of folder
        pr_fld = ls_dt_fld[1]  # pr_fld = id parent

        f = onedrivesdk.Folder()
        i = onedrivesdk.Item()
        i.name = nm_fld
        i.folder = f

        try:
            OB = self.client.item(drive="me", id=pr_fld).children.add(i)
            return OB.id
        except Exception:
            return None

    def delete_item(self, id_one):
        try:
            self.client.item(id=id_one).delete()
            return True
        except Exception:
            return False

    def upload_file(self, ls_dt_it):
        pr_it = ls_dt_it[0]  # pr_it = father id
        nm_it = ls_dt_it[1]  # nm_it = name item to upload
        ph_it = ls_dt_it[2]  # ph_it = local path item to upload

        try:
            OB = self.client.item(drive="me", id=pr_it).children[nm_it].upload(ph_it)
            return OB.id
        except Exception:
            return None

    def dw_file(self, ls_dt_it):
        id_ser = ls_dt_it[0]  # item id on server
        ph_loc = ls_dt_it[1]  # local path

        try:
            self.client.item(id=id_ser).download(ph_loc)
            return True
        except Exception:
            return False

    def get_files(self, it_id='root', ls_fl=[], ph_it='/'):
        try:
            for it in self.navigate(it_id):
                if it.folder is not None:
                    self.get_files(it.id, ls_fl, ph_it + it.name + '/')
                else:
                    ls_fl.append([it.id, it.name, ph_it + it.name])

            return ls_fl
        except Exception as e:
            print('error: {}'.format(e))

    def get_folders(self, it_id='root', ls_fl=[], ph_it='/'):
        try:
            for it in self.navigate(it_id):
                if it.folder is not None:
                    ls_fl.append([it.id, it.name, ph_it + it.name])
                    self.get_folders(it.id, ls_fl, ph_it + it.name + '/')

            return ls_fl
        except Exception as e:
            print('error: {}'.format(e))

    def navigate(self, it_id='root'):
        items = self.client.item(id=it_id).children.get()
        return items

    def get_link_sharing(self, id_oned, action):  # action [1, 2]
        action = "view" if action == 1 else "edit"
        permission = self.client.item(id=id_oned).create_link(action).post()
        return permission.link.web_url

if __name__ == '__main__':
    # ic = 1
    # pa = 'C:/godo-sync/yulimili_21_10@hotmail.com__dropbox__'
    # at = 'foJG6ertFYEAAAAAAAAUbC69UrGK_QTTrsN6qNLHdik5nqtHrlF0pnjmPeMWYUD2'
    # ob = SV_DropBox([ic, 'dropbox', pa, at])
    # ob.connect()
    # # sl = ob.get_folders()
    # sl = ob.get_link_sharing("/FOLDER_01/PD.pdf")
    # print(sl)
    pass
