import pysftp
import fnmatch
import warnings

from config.settings import SFTP_HOST, SFTP_USER, SFTP_PASS, SFTP_PATH

# Supress warning about trusting all host keys - bad practice!
warnings.filterwarnings('ignore','.*Failed to load HostKeys.*')


def list_all_files():
    # Trust all host keys - bad practice!
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None

    # Get connection
    sftp = pysftp.Connection(host=SFTP_HOST, username=SFTP_USER, password=SFTP_PASS, cnopts=cnopts)
    
    # filter away directorires and files without file extensions
    filelist = [ f for f in sftp.listdir(SFTP_PATH) if fnmatch.fnmatch(f, '*.*') ]

    return filelist, sftp
