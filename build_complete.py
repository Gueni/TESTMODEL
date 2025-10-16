import os
import subprocess
import sys
import pkg_resources

def check_dependencies():
    """Check if all required packages are installed"""
    required = [
        'dash', 'plotly', 'pandas', 'numpy', 'flask', 'tkinter'
    ]
    
    missing = []
    for package in required:
        try:
            pkg_resources.get_distribution(package.split('[')[0] if '[' in package else package)
        except pkg_resources.DistributionNotFound:
            missing.append(package)
    
    return missing

def install_dependencies():
    """Install required dependencies"""
    packages = [
        'dash',
        'plotly',
        'pandas',
        'numpy',
        'flask'
    ]
    
    print("Installing dependencies...")
    for package in packages:
        try:
            subprocess.run([sys.executable, '-m', 'pip', 'install', package], check=True)
            print(f"✓ Installed {package}")
        except subprocess.CalledProcessError:
            print(f"✗ Failed to install {package}")

def build_executable():
    """Build the executable"""
    
    # Create the spec file content
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main_launcher.py'],
    pathex=[],
    binaries=[],
    datas=[
    ],
    hiddenimports=[
        'dash', 'plotly', 'pandas', 'numpy', 'flask', 'werkzeug',
        'dash.dcc', 'dash.html', 'dash.dependencies',
        'tkinter', 'tkinter.ttk', 'tkinter.filedialog', 'tkinter.messagebox',
        'json', 'os', 'sys', 'threading', 'webbrowser', 'datetime', 're',
        'itertools', 'collections'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='PYPLECS_Dashboard',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico',
)
'''
    
    # Write spec file
    with open('pyplecs_spec.spec', 'w') as f:
        f.write(spec_content)
    
    # Build with PyInstaller
    cmd = ['pyinstaller', 'pyplecs_spec.spec']
    
    print("Building executable...")
    subprocess.run(cmd, check=True)
    
    # Clean up
    if os.path.exists('pyplecs_spec.spec'):
        os.remove('pyplecs_spec.spec')

def main():
    print("PYPLECS Dashboard EXE Builder")
    print("=" * 40)
    
    # Check dependencies
    missing = check_dependencies()
    if missing:
        print(f"Missing dependencies: {', '.join(missing)}")
        response = input("Do you want to install them? (y/n): ")
        if response.lower() == 'y':
            install_dependencies()
        else:
            print("Cannot proceed without dependencies.")
            return
    
    # Build executable
    build_executable()
    
    print("\\nBuild completed!")
    print("Your executable is located in: dist/PYPLECS_Dashboard.exe")
    print("\\nNote: Make sure the following folders are in the same directory as the EXE:")
    print("  - assets/")
    print("  - CSV_MAPS/")

if __name__ == "__main__":
    main()