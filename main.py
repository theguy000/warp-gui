## main.py
import sys
from PyQt5.QtWidgets import QApplication
from warp_gui import WarpGUI
import warnings
warnings.filterwarnings('ignore')

def main():
    """
    The main entry point of the application that initializes the GUI.
    """
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False) 
    gui = WarpGUI()
    gui.show_main_window()
    sys.exit(app.exec_())
    
if __name__ == '__main__':
    main()
