import pyautogui
import time
import subprocess

# Config - adjust these if needed
plecs_path = r"C:\Program Files\Plexim\PLECS 4.7\plecs.exe"  # Change this to your PLECS path
model_path = r"C:\path\to\your\model.plecs"  # Change this to your model path

# Open PLECS
subprocess.Popen([plecs_path])
time.sleep(5)  # Wait for PLECS to open

# Open the model
pyautogui.hotkey('ctrl', 'o')
time.sleep(1)
pyautogui.write(model_path)
pyautogui.press('enter')
time.sleep(3)  # Wait for model to load

# Click Edit menu
pyautogui.click(100, 20)
time.sleep(1)

# Go down to 15th item (Break all external links)
for i in range(15):
    pyautogui.press('down')
    time.sleep(0.1)
pyautogui.press('enter')
time.sleep(1)  # Wait for dialog to appear

# Move to OK and click (tab twice to get to OK, assuming Cancel is default)
pyautogui.press('tab')  # Move from Cancel to OK
pyautogui.press('tab')  # Sometimes need two tabs
pyautogui.press('enter')

print("Done! Links broken.")