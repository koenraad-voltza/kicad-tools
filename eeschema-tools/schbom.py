import pyautogui
import shlex
import subprocess
import time
import os
import sys

pyautogui.PAUSE = 0.05
filename=sys.argv[1]
subprocess.Popen('eeschema '+filename,shell=True)
time.sleep(4)
pyautogui.hotkey('alt','t')
for i in range(9):
    pyautogui.hotkey('down')
pyautogui.PAUSE = 0.5
pyautogui.hotkey('enter')
pyautogui.PAUSE = 2
pyautogui.hotkey('enter')
pyautogui.PAUSE = 0.1
pyautogui.hotkey('alt','f4')
pyautogui.hotkey('alt','f4')
