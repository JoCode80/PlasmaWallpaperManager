import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QDialog, QPushButton, QFileDialog, QFrame, QCheckBox, QDialogButtonBox, QLabel, QMessageBox
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from password_utils import PasswordDialog, verify_password
from plasma_utils import set_plasma_background
from sddm_utils import create_and_activate_sddm_theme
from splashscreen_utils import update_splashscreen_theme
from lockscreen_utils import update_lockscreen_background

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.password = None
        self.image_path = ""
        self.setWindowTitle("Consistent Wallpaper Changer")
        self.setGeometry(100, 100, 400, 400)

        layout = QVBoxLayout()

        self.selected_image_label = QLabel("No image selected", self)
        self.image_preview = QLabel(self)
        layout.addWidget(self.selected_image_label)
        layout.addWidget(self.image_preview)

        self.select_button = QPushButton("Select Background Image", self)
        self.select_button.clicked.connect(self.select_image)
        layout.addWidget(self.select_button)

        self.select_all_checkbox = QCheckBox("Select All", self)
        self.select_all_checkbox.stateChanged.connect(self.select_all_state_changed)
        layout.addWidget(self.select_all_checkbox)

        horizontal_line = QFrame(self)
        horizontal_line.setFrameShape(QFrame.Shape.HLine)
        horizontal_line.setFrameShadow(QFrame.Shadow.Sunken)
        layout.addWidget(horizontal_line)

        self.desktop_checkbox = QCheckBox("Plasma Desktop", self)
        self.sddm_checkbox = QCheckBox("SDDM Theme (root password required)", self)
        self.splashscreen_checkbox = QCheckBox("Plasma Splashscreen", self)
        self.lockscreen_checkbox = QCheckBox("Lockscreen", self)
        layout.addWidget(self.desktop_checkbox)
        layout.addWidget(self.lockscreen_checkbox)
        layout.addWidget(self.splashscreen_checkbox)
        layout.addWidget(self.sddm_checkbox)

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Cancel | QDialogButtonBox.StandardButton.Ok, self)
        buttons.accepted.connect(self.apply_changes)
        buttons.rejected.connect(self.cancel)
        layout.addWidget(buttons)

        self.setLayout(layout)

    def select_all_state_changed(self, state):
        if state == 2:
            self.desktop_checkbox.setChecked(True)
            self.sddm_checkbox.setChecked(True)
            self.splashscreen_checkbox.setChecked(True)
            self.lockscreen_checkbox.setChecked(True)
        else:
            self.desktop_checkbox.setChecked(False)
            self.sddm_checkbox.setChecked(False)
            self.splashscreen_checkbox.setChecked(False)
            self.lockscreen_checkbox.setChecked(False)

    def select_image(self):
        self.image_path, _ = QFileDialog.getOpenFileName(self, "Select an Image", "", "Images (*.png *.jpg *.jpeg)")
        if self.image_path:
            self.selected_image_label.setText(f"Selected image: {self.image_path}")
            self.show_image_preview(self.image_path)
        else:
            self.selected_image_label.setText("No image selected.")
            self.image_preview.clear()

    def show_image_preview(self, image_path):
        pixmap = QPixmap(image_path)
        self.image_preview.setPixmap(pixmap.scaled(200, 200, aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio))
        self.image_preview.setAlignment(Qt.AlignmentFlag.AlignCenter)

    from PyQt6.QtWidgets import QMessageBox

    def apply_changes(self):
        if not self.image_path:
            QMessageBox.warning(self, "No Image Selected", "Please select an image before applying changes.")
            return

        try:
            if self.desktop_checkbox.isChecked():
                set_plasma_background(self.image_path)

            if self.sddm_checkbox.isChecked():
                if self.password is None:
                    password_dialog = PasswordDialog()
                    if password_dialog.exec() == QDialog.DialogCode.Accepted:
                        self.password = password_dialog.get_password()
                        if not verify_password(self.password):
                            QMessageBox.warning(self, "Invalid Password", "The entered password is invalid. Please try again.")
                            self.password = None
                            return
                    else:
                        QMessageBox.critical(self, "Cancelled", "Password prompt cancelled!")
                        return

                create_and_activate_sddm_theme(self.image_path, self.password)

            if self.splashscreen_checkbox.isChecked():
                if not update_splashscreen_theme(self.image_path):
                    QMessageBox.warning(self, "Error Customizing Splashscreen", "There was an error customizing the Splashscreen.")

            if self.lockscreen_checkbox.isChecked():
                if not update_lockscreen_background(self.image_path):
                    QMessageBox.warning(self, "Error Updating Lockscreen", "There was an error updating the Lockscreen.")

            self.selected_image_label.setText("Changes successfully applied!")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")


    def cancel(self):
        self.close()


def main():
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
