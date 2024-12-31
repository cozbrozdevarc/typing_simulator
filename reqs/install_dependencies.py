import subprocess
import sys
import pkg_resources
import os

def install_requirements():
    """Install required packages from requirements.txt."""
    print("Checking and installing dependencies...")
    
    if not os.path.exists('requirements.txt'):
        print("Error: requirements.txt not found!")
        return False
    
    try:
        with open('requirements.txt', 'r') as f:
            requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]
        
        installed = {pkg.key for pkg in pkg_resources.working_set}
        missing = []
        
        for requirement in requirements:
            package_name = requirement.split('==')[0]
            if package_name.lower() not in installed:
                missing.append(requirement)
        
        if missing:
            print(f"Installing missing packages: {', '.join(missing)}")
            try:
                subprocess.check_call([sys.executable, '-m', 'pip', 'install'] + missing)
                print("All dependencies installed successfully!")
                return True
            except subprocess.CalledProcessError as e:
                print(f"Error installing packages: {str(e)}")
                return False
        else:
            print("All dependencies are already installed!")
            return True
            
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return False

if __name__ == "__main__":
    success = install_requirements()
    if success:
        print("\nYou can now run the application using: python main.py")
    else:
        print("\nFailed to install dependencies. Please install them manually using:")
        print("pip install -r requirements.txt")