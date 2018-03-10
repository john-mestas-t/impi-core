from BL_Local_Engine_Utils import *
from DB_Controlers import *
from DB import *


class LocalEngine():
    def __init__(self):
        pass

    def start_engine(self):
        self.init_database('R')
        self.start_scann_directories()

    def init_database(self, state):
        DB_Item.update_all_status(state)
        # R = remove
        # N = normal
        # I = insert

    def start_scann_directories(self):
        ls_ac = DB_Account.select('all')  # ls_ac = list_accounts
        for ac in ls_ac:
            File_Directoy(ac.id_account, ac.path_account)

if __name__ == '__main__':
    obj = LocalEngine()
    obj.start_engine()
