import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import os
import json

class ConfigWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("PYPLECS Dashboard Configuration")
        
        # Center the window on screen
        self.center_window(600, 350)  # Reduced height since we removed fields
        
        # Initialize variables with your default values
        self.header_path            = tk.StringVar(value=r"")
        self.csv_maps_folder        = tk.StringVar(value=r"")
        self.input_json             = tk.StringVar(value=r"")
        self.port                   = tk.StringVar(value="8050")

        self.create_widgets()
    
    def center_window(self, width=600, height=350):
        """Center the window with specified dimensions"""
        # Get screen dimensions
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Calculate position
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        
        # Set window geometry
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        
        # Optional: Prevent resizing
        self.root.resizable(False, False)
    
    def create_widgets(self):
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(main_frame, text="PYPLECS Dashboard Configuration", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=4, pady=(0, 20))
        
        row = 1
        
        # Header Files Path
        ttk.Label(main_frame, text="Header Files Path:").grid(row=row, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.header_path, width=50).grid(row=row, column=1, columnspan=2, sticky=tk.W+tk.E, padx=5, pady=5)
        ttk.Button(main_frame, text="Browse", command=self.browse_header_path).grid(row=row, column=3, pady=5, padx=(0, 5))
        row += 1
        
        # CSV Maps Folder
        ttk.Label(main_frame, text="CSV Maps Folder:").grid(row=row, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.csv_maps_folder, width=50).grid(row=row, column=1, columnspan=2, sticky=tk.W+tk.E, padx=5, pady=5)
        ttk.Button(main_frame, text="Browse", command=self.browse_csv_maps).grid(row=row, column=3, pady=5, padx=(0, 5))
        row += 1
        
        # Input JSON File
        ttk.Label(main_frame, text="Input JSON File:").grid(row=row, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.input_json, width=50).grid(row=row, column=1, columnspan=2, sticky=tk.W+tk.E, padx=5, pady=5)
        ttk.Button(main_frame, text="Browse", command=self.browse_input_json).grid(row=row, column=3, pady=5, padx=(0, 5))
        row += 1
        
        # Port
        ttk.Label(main_frame, text="Port:").grid(row=row, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.port, width=15).grid(row=row, column=1, sticky=tk.W, padx=5, pady=5)
        # Empty space to maintain alignment
        ttk.Label(main_frame, text="").grid(row=row, column=2)
        ttk.Label(main_frame, text="").grid(row=row, column=3)
        row += 1
        
        # Info label about JSON configuration
        info_text = "Note: permute, harmonics, and Y_Lengths are now configured in the JSON file."
        info_label = ttk.Label(main_frame, text=info_text, font=("Arial", 9), foreground="blue")
        info_label.grid(row=row, column=0, columnspan=4, pady=10)
        row += 1
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=row, column=0, columnspan=4, pady=20)
        
        ttk.Button(button_frame, text="Launch Dashboard", command=self.launch_dashboard).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="Validate Paths", command=self.validate_paths).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="Exit", command=self.root.quit).pack(side=tk.LEFT, padx=10)
        
        # Status label
        self.status_label = ttk.Label(main_frame, text="Ready to launch...", foreground="green")
        self.status_label.grid(row=row+1, column=0, columnspan=4, pady=10)
        
        # Configure grid weights for proper resizing
        main_frame.columnconfigure(0, weight=0)  # Labels column - don't expand
        main_frame.columnconfigure(1, weight=1)  # Entry fields column - expand
        main_frame.columnconfigure(2, weight=0)  # Second part of entry fields
        main_frame.columnconfigure(3, weight=0)  # Buttons column - don't expand
    
    def browse_header_path(self):
        path = filedialog.askdirectory(initialdir=self.header_path.get(), title="Select Header Files Directory")
        if path:
            self.header_path.set(path)
    
    def browse_csv_maps(self):
        path = filedialog.askdirectory(initialdir=self.csv_maps_folder.get(), title="Select CSV Maps Directory")
        if path:
            self.csv_maps_folder.set(path)
    
    def browse_input_json(self):
        path = filedialog.askopenfilename(
            initialdir=os.path.dirname(self.input_json.get()) if self.input_json.get() else "/",
            title="Select Input JSON File",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if path:
            self.input_json.set(path)
    
    def validate_paths(self):
        errors = []
        
        if not os.path.exists(self.header_path.get()):
            errors.append("Header path does not exist")
        if not os.path.exists(self.csv_maps_folder.get()):
            errors.append("CSV maps folder does not exist")
        if not os.path.exists(self.input_json.get()):
            errors.append("Input JSON file does not exist")
        else:
            # Validate that the JSON contains the new fields
            try:
                with open(self.input_json.get(), 'r') as f:
                    json_config = json.load(f)
                
                if 'permute' not in json_config:
                    errors.append("JSON file missing 'permute' field")
                if 'harmonics' not in json_config:
                    errors.append("JSON file missing 'harmonics' field")
                if 'Y_Lengths' not in json_config:
                    errors.append("JSON file missing 'Y_Lengths' field")
                    
            except json.JSONDecodeError:
                errors.append("Invalid JSON file")
            except Exception as e:
                errors.append(f"Error reading JSON file: {str(e)}")
        
        if errors:
            messagebox.showerror("Validation Failed", "\n".join(errors))
            self.status_label.config(text="Validation failed", foreground="red")
        else:
            messagebox.showinfo("Validation Successful", "All paths and JSON configuration are valid!")
            self.status_label.config(text="Validation successful", foreground="green")
    
    def launch_dashboard(self):
        """Launch the Dash dashboard with configured parameters"""
        self.validate_paths()
        self.status_label.config(text="Launching dashboard...", foreground="blue")
        
        # Set environment variables
        os.environ['DASH_HEADER_PATH'] = self.header_path.get()
        os.environ['DASH_CSV_MAPS'] = self.csv_maps_folder.get()
        os.environ['DASH_INPUT_JSON'] = self.input_json.get()
        os.environ['DASH_PORT'] = self.port.get()
        
        # Close the config window
        self.root.destroy()
        
        # Import and run the dashboard
        import main_dashboard
        
        # Open browser after a short delay
        import webbrowser
        import threading
        
        def open_browser():
            import time
            time.sleep(2)
            webbrowser.open_new(f"http://localhost:{os.environ['DASH_PORT']}")
        
        browser_thread = threading.Thread(target=open_browser, daemon=True)
        browser_thread.start()
        
        # Run the dashboard
        print(f"Starting Dash app on port {os.environ['DASH_PORT']}...")
        main_dashboard.app.run(debug=True, port=int(os.environ['DASH_PORT']), use_reloader=False)

if __name__ == "__main__":
    root = tk.Tk()
    app = ConfigWindow(root)
    root.mainloop()