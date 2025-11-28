from typing import Literal

os_type = Literal['Windows', 'Linux']

class Bases:
    def __init__(self, os: os_type):
        self.os: os_type = os

    def get_base_content(self, base_name: str):
        base_dir = ''

        if self.os == 'Windows':
            base_dir = 'windows_bases\\'
        elif self.os == 'Linux':
            base_dir = 'linux_bases/'

        with open(base_dir + base_name, 'r') as f:
            return f.read()

# Usage examples:
# windows_bases = Bases('Windows')
# print(windows_bases.get_path('alt_8_base'))  # C:\Program Files\YourApp\Data

# linux_bases = Bases('Linux')
# print(linux_bases.get_path('alt_8_base'))  # /opt/yourapp/data