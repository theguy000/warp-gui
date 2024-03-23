## warp_gui.py
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QVBoxLayout, QWidget, QMessageBox, QDialog, QInputDialog, QSystemTrayIcon, QMenu, QAction, qApp
from PyQt5.QtGui import QIcon, QPixmap
from warp_controller import WarpController
from settings_dialog import SettingsDialog
import sys

class WarpGUI(QMainWindow):
    def __init__(self):
        super(WarpGUI, self).__init__()
        self.warp_controller = WarpController()
        self.init_ui()
        icon_path = "WarpGui.png"
        self.setWindowIcon(QIcon(QPixmap(icon_path)))
        self.tray_icon = QSystemTrayIcon(QIcon(QPixmap(icon_path)), self)
        self.tray_icon.show()
        self.update_toggle_button(self.warp_controller.check_status())

        
        show_action = QAction("Show", self)
        quit_action = QAction("Quit", self)
        show_action.triggered.connect(self.show)
        quit_action.triggered.connect(qApp.quit)
        tray_menu = QMenu()
        tray_menu.addAction(show_action)
        tray_menu.addAction(quit_action)
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()


        self.warp_cli_path = "warp-cli"  # Default path to the warp-cli executable
        try:
            with open('registration_status.txt', 'r') as file:
                self.is_registered = file.read() == 'True'
        except FileNotFoundError:

        
            self.is_registered = False
    def init_ui(self):
        # Set up the main window
        self.setWindowTitle('Cloudflare WARP Client')
        self.setGeometry(100, 100, 280, 170)
        
        # Create layout and buttons
        layout = QVBoxLayout()
        
        self.toggle_connection_button = QPushButton('Connect', self)
        self.toggle_connection_button.clicked.connect(self.toggle_connection)
        
        
        self.settings_button = QPushButton('Private Key', self)
        self.settings_button.clicked.connect(self.show_settings_dialog)

        # status button here
        self.status_button = QPushButton('Status', self)
        self.status_button.clicked.connect(self.show_status)

        # mode button here
        self.mode_button = QPushButton('Set Mode', self)
        self.mode_button.clicked.connect(self.set_mode)

        # Add buttons to layout in the new order

        layout.addWidget(self.toggle_connection_button)
        layout.addWidget(self.settings_button)
        layout.addWidget(self.status_button)  # Status button added here
        layout.addWidget(self.mode_button)
        # Set central widget and layout
        central_widget = QWidget(self)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)


    def toggle_connection(self):
        if self.warp_controller.check_status():
            # If connected, disconnect
            self.disconnect_client()
            self.update_toggle_button(False)
        else:
            # If disconnected, connect
            self.connect_client()
            self.update_toggle_button(True)

    def update_toggle_button(self, connected):
        if connected:
            self.toggle_connection_button.setText('Disconnect')
            self.toggle_connection_button.setStyleSheet("background-color: green; color: white;")
        else:
            self.toggle_connection_button.setText('Connect')
            self.toggle_connection_button.setStyleSheet("background-color: red; color: white;")

    def show_settings_dialog(self):
        settings_dialog = SettingsDialog(self)
        if settings_dialog.exec() == QDialog.Accepted:
            license_key = settings_dialog.get_license_key()
            if self.warp_controller.set_license(license_key):
                QMessageBox.information(self, 'Success', 'License key set successfully.')
            else:
                QMessageBox.critical(self, 'Error', 'Failed to set license key.')
    
    
    def register_client(self):
        if not self.is_registered:
            if self.warp_controller.registration_new():
                QMessageBox.information(self, 'Success', 'Registration successful.')
                self.is_registered = True
            else:
                QMessageBox.critical(self, 'Error', 'Registration failed.')

    def connect_client(self):
        if not self.is_registered:
            self.register_client()
        if self.warp_controller.connect():
            QMessageBox.information(self, 'Success', 'Connection successful.')
            self.update_toggle_button(True)
        else:
            QMessageBox.critical(self, 'Error', 'Connection failed.')
            self.update_toggle_button(False)

    def disconnect_client(self):
        if self.warp_controller.disconnect():
            QMessageBox.information(self, 'Success', 'Disconnection successful.')
            self.update_toggle_button(False)
        else:
            QMessageBox.critical(self, 'Error', 'Disconnection failed.')
            self.update_toggle_button(True)

    def show_settings_dialog(self):
        settings_dialog = SettingsDialog(self)
        if settings_dialog.exec() == QDialog.Accepted:
            license_key = settings_dialog.get_license_key()
            if self.warp_controller.set_license(license_key):
                QMessageBox.information(self, 'Success', 'License key set successfully.')
            else:
                QMessageBox.critical(self, 'Error', 'Failed to set license key.')
    def show_status(self):
        if self.warp_controller.check_status():
            QMessageBox.information(self, 'Status', 'WARP is currently connected.')
        else:
            QMessageBox.critical(self, 'Status', 'WARP is not connected.')

    def set_mode(self):
        mode, ok = QInputDialog.getItem(self, "Select Mode", "Choose a mode:", ["DNS only mode via DoH", "WARP with DoH"], 0, False)
        if ok and mode:
            mode_key = 'doh' if mode == "DNS only mode via DoH" else 'warp+doh'
            if self.warp_controller.set_mode(mode_key):
                QMessageBox.information(self, 'Success', f'Mode set to {mode}.')
            else:
                QMessageBox.critical(self, 'Error', 'Failed to set mode.')


    def show_main_window(self):
        self.show()

def main():
    app = QApplication(sys.argv)
    gui = WarpGUI()
    gui.show_main_window()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()