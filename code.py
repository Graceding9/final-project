import tkinter as tk
from tkinter import messagebox, simpledialog
import base64
import json
import random
import string
import os

# --- 1. Constants and File Paths (Same as before) ---
DATA_FILE = "password_data.txt"
MASTER_KEY_FILE = "master_key.txt"


# --- 2. Encryption/Decryption Functions (Same as before) ---
def encrypt_data(text):
    encoded_bytes = text.encode('utf-8')
    encoded_b64 = base64.b64encode(encoded_bytes)
    return encoded_b64.decode('utf-8')


def decrypt_data(b64_string):
    try:
        decoded_bytes = base64.b64decode(b64_string)
        return decoded_bytes.decode('utf-8')
    except Exception:
        return ""

    # --- 3. Data Persistence (Same as before) ---


def load_data():
    try:
        with open(DATA_FILE, 'r') as file:
            encrypted_content = file.read()
            if not encrypted_content:
                return {}
            decrypted_content = decrypt_data(encrypted_content)
            return json.loads(decrypted_content)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        messagebox.showerror("Error", "Could not read data file. Data might be corrupted.")
        return {}
    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred: {e}")
        return {}


def save_data(data_dict):
    try:
        json_string = json.dumps(data_dict, indent=4)
        encrypted_content = encrypt_data(json_string)
        with open(DATA_FILE, 'w') as file:
            file.write(encrypted_content)
        return True
    except Exception as e:
        messagebox.showerror("Save Error", f"Could not save data: {e}")
        return False


# --- 4. Master Password Management (Same as before) ---
def setup_master_password(password):
    try:
        encrypted_pass = encrypt_data(password)
        with open(MASTER_KEY_FILE, 'w') as file:
            file.write(encrypted_pass)
        return True
    except Exception:
        return False


def check_master_password(password):
    try:
        with open(MASTER_KEY_FILE, 'r') as file:
            stored_pass_encrypted = file.read()
            stored_pass = decrypt_data(stored_pass_encrypted)
            return password == stored_pass
    except FileNotFoundError:
        return False

    # --- 5. Password Generator (Same as before) ---


def generate_password(length=12):
    letters = list(string.ascii_letters)
    digits = list(string.digits)
    symbols = list(string.punctuation)
    all_chars = letters + digits + symbols
    password_list = [
        random.choice(letters),
        random.choice(digits),
        random.choice(symbols)
    ]
    for _ in range(length - 3):
        password_list.append(random.choice(all_chars))
    random.shuffle(password_list)
    return "".join(password_list)


# --- 6. GUI Application Class ---
class PasswordManagerApp:
    def __init__(self, master):
        self.master = master
        master.title("Python Password Manager")
        self.password_data = {}

        if not os.path.exists(MASTER_KEY_FILE):
            self.show_master_setup()
        else:
            self.show_login()

    def clear_frame(self):
        for widget in self.master.winfo_children():
            widget.destroy()

    # --- Authentication (Same as before) ---
    def show_master_setup(self):
        # ... (setup code remains the same)
        self.clear_frame()
        tk.Label(self.master, text="Set Master Password").grid(row=0, column=0, columnspan=2, pady=10)
        tk.Label(self.master, text="New Password:").grid(row=1, column=0, sticky='w', padx=5)
        self.new_master_entry = tk.Entry(self.master, show="*", width=30)
        self.new_master_entry.grid(row=1, column=1, padx=5, pady=5)
        tk.Button(self.master, text="Set Password", command=self.set_master).grid(row=2, column=0, columnspan=2,
                                                                                  pady=10)

    def set_master(self):
        new_pass = self.new_master_entry.get()
        if new_pass:
            if setup_master_password(new_pass):
                messagebox.showinfo("Success", "Master Password set successfully!")
                self.show_login()
            else:
                messagebox.showerror("Error", "Could not set master password.")
        else:
            messagebox.showerror("Error", "Password cannot be empty.")

    def show_login(self):
        # ... (login code remains the same)
        self.clear_frame()
        tk.Label(self.master, text="Master Password Login").grid(row=0, column=0, columnspan=2, pady=10)
        tk.Label(self.master, text="Password:").grid(row=1, column=0, sticky='w', padx=5)
        self.login_entry = tk.Entry(self.master, show="*", width=30)
        self.login_entry.grid(row=1, column=1, padx=5, pady=5)
        tk.Button(self.master, text="Login", command=self.attempt_login).grid(row=2, column=0, columnspan=2, pady=10)

    def attempt_login(self):
        login_pass = self.login_entry.get()
        if check_master_password(login_pass):
            self.password_data = load_data()
            self.show_main_app()
        else:
            messagebox.showerror("Login Failed", "Incorrect Master Password.")

    # --- Main Application Screen (Layout Updated) ---

    def show_main_app(self):
        """Displays the main password manager interface."""
        self.clear_frame()

        # Row 0, 1, 2: Input fields (Same as screenshot)
        tk.Label(self.master, text="Website:").grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.website_entry = tk.Entry(self.master, width=30)
        self.website_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.master, text="Username/Email:").grid(row=1, column=0, sticky='w', padx=5, pady=5)
        self.username_entry = tk.Entry(self.master, width=30)
        self.username_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self.master, text="Password:").grid(row=2, column=0, sticky='w', padx=5, pady=5)
        self.password_entry = tk.Entry(self.master, show="*", width=30)
        self.password_entry.grid(row=2, column=1, padx=5, pady=5)

        # Row 3: Add/Update and Generate Buttons (Same as screenshot)
        tk.Button(self.master, text="Generate Pass", command=self.fill_generated_password).grid(row=3, column=0,
                                                                                                sticky='w', padx=5,
                                                                                                pady=5, ipadx=10)
        tk.Button(self.master, text="Add/Update Entry", command=self.add_entry).grid(row=3, column=1, sticky='e',
                                                                                     padx=5, pady=5, ipadx=10)

        # --- NEW SECTION: QUERY/VIEW/DELETE BUTTONS (位于 Row 4) ---

        # View All Button
        tk.Button(self.master, text="View All Passwords", command=self.view_all_passwords).grid(row=4, column=0,
                                                                                                sticky='ew', padx=5,
                                                                                                pady=5)

        # Search Button
        tk.Button(self.master, text="Search Website", command=self.search_entry).grid(row=4, column=1, sticky='w',
                                                                                      padx=5, pady=5)

        # Delete Button (New Feature)
        tk.Button(self.master, text="Delete Entry", command=self.delete_entry).grid(row=5, column=0, columnspan=2,
                                                                                    sticky='ew', padx=5, pady=5)

    # --- Core Feature Implementations (Updated) ---

    def fill_generated_password(self):
        # ... (Same as before)
        new_pass = generate_password()
        self.password_entry.delete(0, tk.END)
        self.password_entry.insert(0, new_pass)

    def add_entry(self):
        # ... (Same as before)
        website = self.website_entry.get().strip()
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not website or not username or not password:
            messagebox.showerror("Error", "All fields must be filled.")
            return

        encrypted_password = encrypt_data(password)
        self.password_data[website] = {
            "username": username,
            "password": encrypted_password
        }

        if save_data(self.password_data):
            messagebox.showinfo("Success", f"Entry for '{website}' added/updated successfully.")
            self.website_entry.delete(0, tk.END)
            self.username_entry.delete(0, tk.END)
            self.password_entry.delete(0, tk.END)

    def search_entry(self):
        # ... (Same as before)
        website_to_find = simpledialog.askstring("Search", "Enter website name:")
        if not website_to_find:
            return

        if website_to_find in self.password_data:
            entry = self.password_data[website_to_find]
            decrypted_pass = decrypt_data(entry["password"])

            self.show_view_window(
                f"Website: {website_to_find}\nUsername: {entry['username']}\nPassword: {decrypted_pass}",
                f"Search Result: {website_to_find}"
            )
        else:
            messagebox.showerror("Not Found", f"No entry found for '{website_to_find}'.")

    def view_all_passwords(self):
        # ... (Same as before)
        output = "--- All Stored Passwords ---\n\n"
        for website, data in self.password_data.items():
            decrypted_pass = decrypt_data(data["password"])
            output += f"Website: {website}\n"
            output += f"  User: {data['username']}\n"
            output += f"  Pass: {decrypted_pass}\n"
            output += "--------------------------\n"

        self.show_view_window(output, "All Passwords")

    def show_view_window(self, content, title):
        # ... (Same as before)
        view_window = tk.Toplevel(self.master)
        view_window.title(title)
        scrollbar = tk.Scrollbar(view_window)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        text_area = tk.Text(view_window, wrap="word", height=20, width=60, yscrollcommand=scrollbar.set)
        text_area.insert(tk.END, content)
        text_area.config(state=tk.DISABLED)
        text_area.pack(padx=10, pady=10)
        scrollbar.config(command=text_area.yview)

    # --- NEW FEATURE: Delete Entry ---
    def delete_entry(self):
        """Prompts for a website and deletes the entry."""
        website_to_delete = simpledialog.askstring("Delete Entry", "Enter website name to delete:")

        if not website_to_delete:
            return

        if website_to_delete in self.password_data:
            confirm = messagebox.askyesno(
                "Confirm Delete",
                f"Are you sure you want to delete the entry for '{website_to_delete}'?"
            )

            if confirm:
                del self.password_data[website_to_delete]  # 删除 Dictionary 条目
                if save_data(self.password_data):
                    messagebox.showinfo("Success", f"Entry for '{website_to_delete}' deleted and saved.")
        else:
            messagebox.showerror("Not Found", f"No entry found for '{website_to_delete}'.")


# --- Main Program Execution (Same as before) ---

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordManagerApp(root)
    root.mainloop()