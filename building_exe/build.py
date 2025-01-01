# Running this script to build the app is optional, I'm doing it to offer an executable version for anyone who'd prefer it.

import PyInstaller.__main__
import os
import shutil
import time
import threading
import itertools
import sys
from datetime import datetime

class LoadingSpinner:
    def __init__(self, description="Loading"):
        self.description = description
        self.spinner = itertools.cycle(['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏'])
        self.busy = False
        self.spinner_thread = None

    def spinner_task(self):
        while self.busy:
            sys.stdout.write(f'\r{next(self.spinner)} {self.description}')
            sys.stdout.flush()
            time.sleep(0.1)
        sys.stdout.write('\r')
        sys.stdout.flush()

    def __enter__(self):
        self.busy = True
        self.spinner_thread = threading.Thread(target=self.spinner_task)
        self.spinner_thread.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.busy = False
        time.sleep(0.1)
        if self.spinner_thread:
            self.spinner_thread.join()
        if exc_type is not None:
            return False
        return True

def build_app():
    print("Starting build process...\n")
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    print(f"Script directory: {script_dir}")
    print(f"Initial working directory: {os.getcwd()}")
    os.chdir(script_dir) 
    print(f"New working directory: {os.getcwd()}")

    #icon_path = "executable_folder/icon/typingmockericon.ico"
    #print(f"Icon path: {icon_path}")
    #print(f"Icon exists: {os.path.exists(icon_path)}")
    
    with LoadingSpinner("Building executable... This may take a few minutes"):
        if os.path.exists('TypingMocker.exe'):
            os.remove('TypingMocker.exe')
        if os.path.exists('TypingMocker.spec'):
            os.remove('TypingMocker.spec')
        if os.path.exists('dist'):
            shutil.rmtree('dist')
        if os.path.exists('build'):
            shutil.rmtree('build')
            
        PyInstaller.__main__.run([
            os.path.abspath('../main.py'),
            '--onefile',
            '--name=TypingMocker',
            f'--add-data={os.path.abspath("../typing_automation")};typing_automation',
            f'--add-data={os.path.abspath("../typing_settings.json")};.',
            '--distpath=dist',
            #f'--icon={icon_path}',
            '--clean',
            '--noupx',
        ])
    
    
    exe_name = "TypingMocker.exe" if os.name == 'nt' else "TypingMocker"
    destination_folder = os.path.join(os.getcwd(), "executable_folder")

    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    exe_path = os.path.join("dist", exe_name)
    final_exe_path = os.path.join(destination_folder, exe_name)
    
    if os.path.exists(exe_path):
        shutil.move(exe_path, final_exe_path)
        with LoadingSpinner("Cleaning up"):
            if os.path.exists('build'):
                shutil.rmtree('build')
            if os.path.exists('dist'):
                shutil.rmtree('dist')
            if os.path.exists('TypingMocker.spec'):
                os.remove('TypingMocker.spec')
        
        print("\n✨ Build complete! ✨")
        print(f"📁 Executable has been moved to: {final_exe_path}")
        print(f"▶️  You can run {exe_name} from the executable_folder directory.")
    else:
        print("\n❌ Error: Executable was not created successfully.")

if __name__ == "__main__":
    try:
        build_app()
    except KeyboardInterrupt:
        print("\n\n🛑 Build process interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ An error occurred during the build process: {str(e)}")
        sys.exit(1)
