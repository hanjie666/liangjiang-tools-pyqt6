#!/usr/bin/env python3
import os
import sys
import platform
import subprocess
import shutil

def create_icon_files():
    """
    Placeholder for icon creation. In a real scenario, you would convert
    your logo to the appropriate formats for Windows (.ico) and macOS (.icns)
    """
    print("Note: You need to create icon files manually:")
    print("- app_icon.ico for Windows")
    print("- app_icon.icns for macOS")
    
    # Create empty icon files for the build process
    if not os.path.exists('app_icon.ico'):
        open('app_icon.ico', 'w').close()
    if not os.path.exists('app_icon.icns'):
        open('app_icon.icns', 'w').close()

def install_dependencies():
    """Install required dependencies"""
    print("Installing dependencies...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-e", "."])
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])

def package_application():
    """Package the application using PyInstaller"""
    print("Packaging application...")
    
    # Run PyInstaller with the spec file
    subprocess.check_call([
        "pyinstaller",
        "--clean",
        "liangjiang_tools.spec"
    ])
    
    # Determine the output directory based on the platform
    if platform.system() == "Darwin":  # macOS
        output_dir = "dist/良匠工具箱.app"
    else:  # Windows
        output_dir = "dist/良匠工具箱"
    
    print(f"Application packaged successfully in: {output_dir}")

def create_distribution_archive():
    """Create a zip archive of the packaged application"""
    print("Creating distribution archive...")
    
    # Determine the archive name based on the platform
    system = platform.system()
    if system == "Darwin":  # macOS
        archive_name = "良匠工具箱-macOS"
        app_path = "dist/良匠工具箱.app"
    else:  # Windows
        archive_name = "良匠工具箱-Windows"
        app_path = "dist/良匠工具箱"
    
    # Create the archive
    shutil.make_archive(archive_name, 'zip', os.path.dirname(app_path), os.path.basename(app_path))
    
    print(f"Distribution archive created: {archive_name}.zip")

def main():
    """Main function to run the packaging process"""
    print(f"Packaging for {platform.system()}...")
    
    # Create icon files
    create_icon_files()
    
    # Install dependencies
    install_dependencies()
    
    # Package the application
    package_application()
    
    # Create distribution archive
    create_distribution_archive()
    
    print("Packaging completed successfully!")

if __name__ == "__main__":
    main() 