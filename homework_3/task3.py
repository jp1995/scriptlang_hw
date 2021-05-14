"""Homework 3, part 3."""

import os
import pwd
import json


class Dir2Json:
    def __init__(self, path):
        """Class constructor."""
        os.chdir(path)
        self.path = path

    def parent(self):
        """Generate parent dictionary."""
        parent_dict = {'name': os.path.basename(self.path),
                       'path': self.path,
                       'mask': oct(os.stat(os.curdir).st_mode)[-3:],
                       'owner': pwd.getpwuid(os.stat(os.curdir).st_uid).pw_name,
                       'type': 'directory',
                       'children': self.children()}
        return parent_dict

    def children(self):
        """Recursively check and generate all child dictionaries."""
        listy = []
        for i in os.listdir():
            if os.path.islink(i):
                continue

            child_dict = {'name': i,
                          'path': f'{os.curdir}/{i}',
                          'mask': oct(os.stat(i).st_mode)[-3:],
                          'owner': pwd.getpwuid(os.stat(i).st_uid).pw_name,
                          'type': self.checktype(i)}

            if child_dict['type'] == 'directory':
                os.chdir(i)
                child_dict['children'] = self.children()
                os.chdir('..')

            listy.append(child_dict)
        return listy

    @staticmethod
    def checktype(item):
        """Check if item is directory or file."""
        if os.path.isdir(item):
            return 'directory'
        else:
            return 'file'

    def __repr__(self):
        """Return output in json format."""
        json_formatted = json.dumps(self.parent(), indent=4)
        return json_formatted


if __name__ == '__main__':
    task = Dir2Json('/home/johan/test')
    task.__repr__()
    print(task)
