import os
from cx_Freeze import setup, Executable
import sys

os.environ['TCL_LIBRARY'] = 'C://Users//vince//anaconda3//tcl//tcl8.6'
os.environ['TK_LIBRARY'] = 'C://Users//vince//anaconda3//tcl//tk8.6'


base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="Parkinson Detector",
    version="0.1",
    description="Détecte si une personne à Parkinson via un fichier audio .wav",
    executables=[Executable("FrontEnd/main.py")], requires=['pyaudio']
)
