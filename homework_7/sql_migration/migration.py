import os
from dotenv import load_dotenv

load_dotenv()
local_user = os.environ.get('LOCAL_USER')
local_pass = os.environ.get('LOCAL_PASS')
local_db = os.environ.get('LOCAL_DB')

remote_user = os.environ.get('REMOTE_USER')
remote_pass = os.environ.get('REMOTE_PASS')
remote_host = os.environ.get('REMOTE_HOST')
remote_db = os.environ.get('REMOTE_DB')

os.system(f"mysqldump -u {local_user} -p{local_pass} {local_db} > dump.sql")
os.system(f'mysql --host={remote_host} --user={remote_user} --password={remote_pass} --database={remote_db} < dump.sql')
os.remove('dump.sql')

print('Migration to remote successful')
