## settings_dialog.py
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout

class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super(SettingsDialog, self).__init__(parent)
        self.setWindowTitle("Settings")
        self.license_key = ""
        self.init_ui()

    def init_ui(self):
        # Create layout and widgets
        layout = QVBoxLayout(self)
        license_key_label = QLabel("License Key:", self)
        self.license_key_edit = QLineEdit(self)
        self.license_key_edit.setPlaceholderText("Enter your license key here")
        
        # Set default value for license key if needed
        self.license_key_edit.setText(self.license_key)
        
        # Buttons
        buttons_layout = QHBoxLayout()
        ok_button = QPushButton("OK", self)
        cancel_button = QPushButton("Cancel", self)
        
        # Connect buttons to their functions
        ok_button.clicked.connect(self.accept)
        cancel_button.clicked.connect(self.reject)
        
        # Add widgets to layout
        layout.addWidget(license_key_label)
        layout.addWidget(self.license_key_edit)
        buttons_layout.addWidget(ok_button)
        buttons_layout.addWidget(cancel_button)
        layout.addLayout(buttons_layout)
        
        # Set dialog layout
        self.setLayout(layout)

    def exec(self) -> int:
        """
        Execute the settings dialog.
        
        :return: QDialog.Accepted or QDialog.Rejected
        """
        result = super(SettingsDialog, self).exec()
        if result == QDialog.Accepted:
            self.license_key = self.license_key_edit.text()
        return result

    def get_license_key(self) -> str:
        """
        Get the entered license key.
        
        :return: The license key as a string
        """
        return self.license_key
