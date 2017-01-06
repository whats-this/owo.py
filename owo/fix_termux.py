#!/data/data/com.termux/files/usr/bin/env python3.5

"""
Used to fix termux shebangs
"""

import os


def main():
    os.system("termux-fix-shebang /data/data/com.termux/files/usr/bin/owo")
    os.system("termux-fix-shebang /data/data/com.termux/files/usr/bin/owo-bg")


if __name__ == '__main__':
    main()
