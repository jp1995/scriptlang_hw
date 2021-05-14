"""Homework 3, part 2."""

import os
import time
import dropbox
from datetime import datetime, timedelta


class MoveOldFiles:
    def __init__(self, path: str):
        """Class constructor."""
        os.chdir(path)
        dbx = dropbox.Dropbox(self.authenticate())
        self.path = path
        self.dbx = dbx

    def authenticate(self):
        """Get token from file."""
        with open(f'/home/johan/scriptlang_homeworks/homework-assignment-3-jp1995/dbx_token.ini', 'r') as file:
            access_token = file.readline()
        return access_token

    def check(self):
        """Check if file is older than 7 days, read and upload to dropbox if so."""
        for i in os.listdir():
            modified = time.ctime(os.path.getmtime(i))
            timecheck = datetime.now() - datetime.strptime(modified, "%c")
            if timecheck > timedelta(days=7):
                with open(i, 'rb') as file:
                    self.dbx.files_upload(file.read(), f'/homework3_task2/{i}')
                os.remove(i)


if __name__ == '__main__':
    check_dir = '/home/johan/scriptlang_homeworks/homework-assignment-3-jp1995/task2_files'
    task = MoveOldFiles(check_dir)
    task.check()



