import os
import shutil
from pathlib import Path

def move_files_from_subfolders_to_root():
    # Define source directory (Downloads folder)
    source_dir = Path(r"C:\Users\msi\Downloadsy")
    
    # Get all files from subfolders
    for root, dirs, files in os.walk(source_dir):
        current_path = Path(root)
        
        # Skip the root directory itself
        if current_path == source_dir:
            continue
            
        # Process each file in the current subfolder
        for file in files:
            source_file = current_path / file
            
            # Create new filename if file already exists in destination
            dest_file = source_dir / file
            counter = 1
            while dest_file.exists():
                name_parts = os.path.splitext(file)
                dest_file = source_dir / f"{name_parts[0]}_{counter}{name_parts[1]}"
                counter += 1
            
            # Move the file
            try:
                shutil.move(str(source_file), str(dest_file))
                print(f"Moved: {source_file} -> {dest_file}")
            except Exception as e:
                print(f"Error moving {source_file}: {e}")
    
    print("\nOperation completed!")

def main():
    print("This script will move all files from subfolders to the main Downloads folder.")
    print(f"Source: C:\\Users\\msi\\Downloads\\**")
    print(f"Destination: C:\\Users\\msi\\Downloads\\")
    print("\nWarning: Files with duplicate names will be renamed.")
    
    confirm = input("\nDo you want to proceed? (yes/no): ").strip().lower()
    
    if confirm in ['yes', 'y']:
        move_files_from_subfolders_to_root()
    else:
        print("Operation cancelled.")

if __name__ == "__main__":
    main()