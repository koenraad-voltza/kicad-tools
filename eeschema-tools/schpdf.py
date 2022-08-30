import pyautogui
import shlex
import subprocess
import time
import os
import sys

pyautogui.PAUSE = 0.05
filename=sys.argv[1]
subprocess.Popen('eeschema '+filename,shell=True)
time.sleep(6)
pyautogui.hotkey('alt','f')
for i in range(11):
    pyautogui.hotkey('down')
pyautogui.PAUSE = 0.5
pyautogui.hotkey('enter')
pyautogui.PAUSE = 2
pyautogui.hotkey('enter')
pyautogui.PAUSE = 0.1
pyautogui.hotkey('alt','f4')
pyautogui.hotkey('alt','f4')
