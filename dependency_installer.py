import sys
import subprocess

def main():
    # implement pip as a subprocess:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
    
if(__name__ == "__main__"):
    main()