import os
import time
import pyautogui
import pygetwindow as gw
import win32gui
import win32con

model_path = r"C:\path\to\your\model.plecs"
model_name = os.path.basename(model_path).replace('.plecs', '')

os.startfile(model_path)
time.sleep(3)

# Print all windows to debug
print("All windows with 'PLECS' in title:")
plecs_windows = gw.getWindowsWithTitle('PLECS')
for i, window in enumerate(plecs_windows):
    print(f"Window {i}: {window}")

if plecs_windows:
    # Just use the first PLECS window (most reliable)
    target_window = plecs_windows[0]
    print(f"Using window: {target_window}")
    
    # Get handle using win32gui
    def enum_windows_callback(hwnd, windows):
        if win32gui.IsWindowVisible(hwnd):
            window_text = win32gui.GetWindowText(hwnd)
            if 'PLECS' in window_text:
                windows.append((hwnd, window_text))
        return True
    
    windows = []
    win32gui.EnumWindows(enum_windows_callback, windows)
    
    # Find matching window
    for hwnd, title in windows:
        if model_name.lower() in title.lower():
            print(f"Found matching window: {title}")
            win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
            win32gui.SetForegroundWindow(hwnd)
            time.sleep(1)
            break
    else:
        # If no match, use first PLECS window
        hwnd = windows[0][0]
        win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
        win32gui.SetForegroundWindow(hwnd)
        time.sleep(1)
else:
    print("No PLECS windows found")