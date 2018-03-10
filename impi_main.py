from BL_Local_Engine import *
from BL_Server_Engine import *


if __name__ == '__main__':
    ob_loc = LocalEngine()
    ob_ser = ServerEngine("personal")
    ob_sha = ServerEngine("sharing")
    a = 0;

    while a == 0:
        print('impi-running')
        ob_loc.start_engine()
        ob_ser.start_engine()
        #ob_sha.start_engine()
        a = a + 0
