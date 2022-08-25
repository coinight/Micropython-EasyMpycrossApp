import subprocess
import os
title = os.getcwd()+'\\title.png'
app = os.getcwd()+'\\main.py'
subprocess.run('pip install pyinstaller')
subprocess.run('pyinstaller -F -w -i '+title+' '+app)
