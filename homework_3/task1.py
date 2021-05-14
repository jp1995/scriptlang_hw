"""Homework 3, part 1."""

import os
import notify2
from pathlib import Path


class Permissions:
    def __init__(self, path: str):
        """Class constructor."""
        self.path = path
        os.chdir(path)
        notify2.init("task1")

    def execute(self):
        """Look for files with full permissions, notify administrator and delete."""
        for file in os.listdir():
            perms = oct(os.stat(file).st_mode)[-3:]
            if perms == '777':
                notice = notify2.Notification('Warning', f'{Path(file).owner()} is trying to '
                                                         f'create a file with full permissions in {os.getcwd()}')
                notice.show()
                os.remove(file)


if __name__ == '__main__':
    task = Permissions('/home/johan/')
    task.execute()
