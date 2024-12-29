import subprocess
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton

class PasswordDialog(QDialog):
    def __init__(self):
        super().__init__()
        # Set the window title
        self.setWindowTitle("Password Prompt")
        # Set the window geometry (position and size)
        self.setGeometry(100, 100, 300, 150)

        # Create layout for the dialog
        layout = QVBoxLayout()

        # Label prompting user for password input
        self.label = QLabel("Please enter your password:")
        layout.addWidget(self.label)

        # Create a password input field (hidden text)
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.password_input)

        # Button to submit the password
        self.submit_button = QPushButton("Confirm")
        self.submit_button.clicked.connect(self.accept)
        layout.addWidget(self.submit_button)

        # Set the layout for the dialog window
        self.setLayout(layout)

    def get_password(self):
        # Return the entered password text
        return self.password_input.text()


def verify_password(password):
    try:
        # Command to check the password with sudo
        command = "sudo -S -k true"
        process = subprocess.run(
            command,
            shell=True,
            text=True,
            input=password + "\n",  # Send the password input to the command
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        # Return True if the command executed successfully
        return process.returncode == 0
    except Exception as e:
        # Handle unexpected errors
        print(f"Unexpected error: {e}")
        return False
