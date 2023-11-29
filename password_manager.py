import json
from cryptography.fernet import Fernet
import tkinter as tk
from tkinter import messagebox, simpledialog

class PasswordManager:
    def __init__(self, key_file='key.key', data_file='passwords.json'):
        self.key_file = key_file
        self.data_file = data_file
        self.load_key()

    def load_key(self):
        try:
            with open(self.key_file, 'rb') as key_file:
                self.key = key_file.read()
        except FileNotFoundError:
            self.generate_key()

    def generate_key(self):
        self.key = Fernet.generate_key()
        with open(self.key_file, 'wb') as key_file:
            key_file.write(self.key)

    def encrypt_data(self, data):
        cipher_suite = Fernet(self.key)
        encrypted_data = cipher_suite.encrypt(data.encode())
        return encrypted_data

    def decrypt_data(self, encrypted_data):
        cipher_suite = Fernet(self.key)
        decrypted_data = cipher_suite.decrypt(encrypted_data).decode()
        return decrypted_data

    def read_passwords(self):
        try:
            with open(self.data_file, 'rb') as file:
                encrypted_data = file.read()
                if encrypted_data:
                    decrypted_data = self.decrypt_data(encrypted_data)
                    return json.loads(decrypted_data)
                else:
                    return {}
        except FileNotFoundError:
            return {}

    def write_passwords(self, passwords):
        encrypted_data = self.encrypt_data(json.dumps(passwords))
        with open(self.data_file, 'wb') as file:
            file.write(encrypted_data)

    def get_password(self, service):
        passwords = self.read_passwords()
        return passwords.get(service, "Password not found.")

    def set_password(self, service, password):
        passwords = self.read_passwords()
        passwords[service] = password
        self.write_passwords(passwords)
        return f"Password for {service} set successfully."


# password_manager.py (enhanced GUI)

import tkinter as tk
from tkinter import messagebox, simpledialog

class PasswordManagerGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Password Manager")

        self.password_manager = PasswordManager()

        self.label = tk.Label(master, text="Service:", font=("Helvetica", 14))
        self.label.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)

        self.service_entry = tk.Entry(master, font=("Helvetica", 14))
        self.service_entry.grid(row=0, column=1, padx=10, pady=10, sticky=tk.W)

        self.get_button = tk.Button(master, text="Get Password", command=self.get_password, font=("Helvetica", 12))
        self.get_button.grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)

        self.set_button = tk.Button(master, text="Set Password", command=self.set_password, font=("Helvetica", 12))
        self.set_button.grid(row=1, column=1, padx=10, pady=10, sticky=tk.W)

    def get_password(self):
        service = self.service_entry.get()
        password = self.password_manager.get_password(service)
        messagebox.showinfo("Password", f"Password for {service}: {password}")

    def set_password(self):
        service = self.service_entry.get()
        password = simpledialog.askstring("Set Password", f"Enter the password for {service}:", show='*')
        if password is not None:
            result = self.password_manager.set_password(service, password)
            messagebox.showinfo("Password Set", result)


def main():
    root = tk.Tk()
    app = PasswordManagerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()


