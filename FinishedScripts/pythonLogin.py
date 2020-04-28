import os
import pyautogui
import time

login='xkcd12345'
password='IB090517'

#stars TWS
os.startfile('C:\Jts\\tws.exe')

while pyautogui.getActiveWindowTitle() != "Login":
    time.sleep(.5)

pyautogui.write(login)
pyautogui.press('tab')
pyautogui.write(password)
time.sleep(.5)
pyautogui.press('enter')

while pyautogui.getActiveWindowTitle() != "Second Factor Authentication":
    time.sleep(.5)

pyautogui.press('tab')

pyautogui.press('space')

while pyautogui.getActiveWindowTitle() != "U2359138 Interactive Brokers":
    #print(pyautogui.getActiveWindowTitle()) cute bit of status update code
    time.sleep(.5)

print("done")

