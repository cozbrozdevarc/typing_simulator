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
    
    build_folder = os.path.join(os.getcwd(), 'build')
    os.makedirs(build_folder, exist_ok=True)
    
    with LoadingSpinner("Building executable... This may take a few minutes"):
        PyInstaller.__main__.run([
            'main.py',
            '--onefile',
            '--name=TypingAutomation',
            '--add-data=src;src',
            '--clean',
            '--noupx',
        ])
    
    exe_name = "TypingAutomation.exe" if os.name == 'nt' else "TypingAutomation"
    exe_path = os.path.join(os.getcwd(), 'dist', exe_name)
    
    if os.path.exists(exe_path):
        with LoadingSpinner("Organizing files"):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            new_folder = os.path.join(build_folder, f"TypingAutomation_{timestamp}")
            os.makedirs(new_folder, exist_ok=True)
            
            new_exe_path = os.path.join(new_folder, exe_name)
            shutil.move(exe_path, new_exe_path)
            
            shutil.rmtree('dist', ignore_errors=True)
            shutil.rmtree('build', ignore_errors=True)
        
        print("\n✨ Build complete! ✨")
        print(f"📁 Executable has been moved to: {new_folder}")
        print(f"▶️  You can run {exe_name} from that location.")
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