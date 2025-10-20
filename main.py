import tkinter as tk
from config_launcher import ConfigWindow
import os
import sys

def main():
    # Add the current directory to Python path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, current_dir)
    
    root = tk.Tk()
    app = ConfigWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()