import os
import subprocess

import mpy_cross

name = os.getcwd() + '\\main.py'
icon = os.getcwd() + '\\title.png'
subprocess.run(
    f'pyinstaller -F -i {icon} {name} --add-data "{mpy_cross.mpy_cross};.\\mpy_cross" --add-data "{icon};." --clean')
