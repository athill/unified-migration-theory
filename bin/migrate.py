
# usage: migrate [project] [migration]

import sys
import paramiko
import os
import json
import errno
import time
from pprint import pprint
import shutil 
from datetime import datetime
import getpass
# pw = getpass.getpass()
# print pw
# exit(2)


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise

# # #
def rexists(sftp, path):
    """os.path.exists for paramiko's SCP object
       http://stackoverflow.com/questions/850749/check-whether-a-path-exists-on-a-remote-host-using-paramiko
    """
    try:
        sftp.stat(path)
    except IOError, e:
        if e.errno == errno.ENOENT:
            return False
        raise
    else:
        return True        

def rmkdir_p(sftp, root, path):
    chkpath = root
    path_array = path.split(os.sep)
    pprint(path_array)
    for part in path_array:
        chkpath = os.path.join(chkpath, part)
        try:
            sftp.stat(path)
        except IOError, e:
            if e.errno == errno.ENOENT:
                sftp.mkdir(chkpath, 0755)

paramiko.util.log_to_file('/tmp/paramiko.log')

home = os.path.expanduser("~")

app = ''
migration = ''
approot = os.path.join(home, 'sites');
# # # Handle command line args
# http://www.diveintopython.net/scripts_and_streams/command_line_arguments.html
# for arg in sys.argv:
    # print arg
if len(sys.argv) < 3:
	print "Usage: migrate [app] [migration]"
	exit(2)

app = sys.argv[1]
migration = sys.argv[2]
# print app + ' ' + migration


# # # Load config
properties_file = os.path.join(approot, app, 'properties.json')
print properties_file
properties_json = open(properties_file)
config = json.load(properties_json)
# pprint(config)
properties_json.close()



# # # Migration file
migration_file = os.path.join(approot, app, 'migrations', migration, 'def.txt')


# # # Build Migration data structure
migrations = {
	"add": [],
	"modify": [],
	"delete": []
}
lines = [line.strip() for line in open(migration_file)]

for line in lines:
	if line == '':
		 continue
	# print line
	action = line[0]
	filen = line[1:].strip()
	if action == 'A':
		migrations["add"].append(filen)
	elif action == 'M':
		migrations["modify"].append(filen)
	else:
		migrations["delete"].append(filen)

# # # # SFTP
# # Open a transport
transport = paramiko.Transport((config['host'], config['port']))
# # # Auth
transport.connect(username = config['username'], password = config['password'])
# # # Go!
sftp = paramiko.SFTPClient.from_transport(transport)

# # # # Backup
backup_dir =  os.path.join(approot, app, 'migrations', migration, 'backup')
for filen in migrations["delete"]+migrations["modify"]:
	d = os.path.join(backup_dir, os.path.dirname(filen))
	print d
	mkdir_p(d)
	rfile = os.path.join(config["remoteroot"], filen)
	if rexists(sftp, rfile):
		sftp.get(rfile, os.path.join(backup_dir, filen))

# # # # Delete -- move after update?
for filen in migrations["delete"]:
	rfile = os.path.join(config["remoteroot"], filen)
	if rexists(sftp, rfile):
		sftp.get(rfile, os.path.join(backup_dir, filen))

# # # # Update
for filen in migrations["add"]+migrations["modify"]:
    rdir = os.path.join(config["remoteroot"], os.path.dirname(filen))
    if not rexists(sftp, rdir):
        rmkdir_p(sftp, config["remoteroot"], os.path.dirname(filen))
    print filen
    sftp.put(os.path.join(config["localroot"], filen), os.path.join(config["remoteroot"], filen))

# # # Close
sftp.close()
transport.close()

# # # Archive migration
# http://docs.python.org/2/library/shutil.html#archiving-operations
localtime   = time.localtime()
timeString  = time.strftime("%Y%m%d", localtime)
print timeString
archive_name = timeString + '_' + migration
root_dir = os.path.join(approot, app, 'migrations')
base_dir = os.path.join(root_dir, migration)
archive_dir = os.path.join(root_dir, str(datetime.now().year))
if not os.path.exists(archive_dir):
    os.makedirs(archive_dir)
shutil.make_archive(os.path.join(archive_dir, archive_name), 'gztar', root_dir, base_dir)
shutil.rmtree(base_dir)





# # # # transport.connect using key: Not working (complaining that it's encrypted)
# # privatekeyfile = os.path.expanduser('~/.ssh/id_rsa')
# # mykey = paramiko.RSAKey.from_private_key_file(privatekeyfile)
# # transport.connect(username = username, pkey = mykey)
