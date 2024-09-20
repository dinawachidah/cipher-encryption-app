import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import numpy as np

def vigenere_cipher(text, key, mode='encrypt'):
    result = []
    key_length = len(key)
    key = key.upper()
    for i, char in enumerate(text):
        if char.isalpha():
            shift = ord(key[i % key_length]) - ord('A')
            if mode == 'decrypt':
                shift = -shift
            if char.isupper():
                result.append(chr((ord(char) - ord('A') + shift) % 26 + ord('A')))
            else:
                result.append(chr((ord(char) - ord('a') + shift) % 26 + ord('a')))
        else:
            result.append(char)
    return ''.join(result)

def create_playfair_matrix(key):
    key = key.upper().replace("J", "I")
    matrix = []
    for char in key + "ABCDEFGHIKLMNOPQRSTUVWXYZ":
        if char not in matrix:
            matrix.append(char)
    return [matrix[i:i+5] for i in range(0, 25, 5)]

def find_position(matrix, char):
    for i, row in enumerate(matrix):
        if char in row:
            return i, row.index(char)
    return None

def playfair_cipher(text, key, mode='encrypt'):
    matrix = create_playfair_matrix(key)
    text = text.upper().replace("J", "I")
    if len(text) % 2 != 0:
        text += 'X'
    
    result = []
    for i in range(0, len(text), 2):
        a, b = text[i], text[i+1]
        row1, col1 = find_position(matrix, a)
        row2, col2 = find_position(matrix, b)
        
        if row1 == row2:
            if mode == 'encrypt':
                result.extend([matrix[row1][(col1+1)%5], matrix[row2][(col2+1)%5]])
            else:
                result.extend([matrix[row1][(col1-1)%5], matrix[row2][(col2-1)%5]])
        elif col1 == col2:
            if mode == 'encrypt':
                result.extend([matrix[(row1+1)%5][col1], matrix[(row2+1)%5][col2]])
            else:
                result.extend([matrix[(row1-1)%5][col1], matrix[(row2-1)%5][col2]])
        else:
            result.extend([matrix[row1][col2], matrix[row2][col1]])
    
    return ''.join(result)

def hill_cipher(text, key, mode='encrypt'):
    # Cek panjang kunci harus minimal 12 karakter
    if len(key) < 12:
        messagebox.showerror("Error", "Kunci untuk Hill Cipher harus minimal 12 karakter")
        return
    
    # Ambil 9 karakter pertama untuk Hill Cipher
    key = key[:9]
    
    # Convert key into 3x3 matrix
    key_matrix = np.array([ord(c) - ord('A') for c in key.upper()]).reshape(3, 3)
    
    text = text.upper()
    result = []
    
    # Process text in chunks of 3
    for i in range(0, len(text), 3):
        chunk = text[i:i+3].ljust(3, 'X')  # Pad the chunk to length 3 if necessary
        chunk_vector = np.array([ord(c) - ord('A') for c in chunk])
        
        if mode == 'encrypt':
            encrypted_vector = np.dot(key_matrix, chunk_vector) % 26
        else:
            try:
                # Calculate inverse of the key matrix
                key_matrix_inv = np.linalg.inv(key_matrix)
                key_matrix_inv = (key_matrix_inv * np.linalg.det(key_matrix)).astype(int) % 26
                encrypted_vector = np.dot(key_matrix_inv, chunk_vector) % 26
            except np.linalg.LinAlgError:
                messagebox.showerror("Error", "Matriks kunci tidak valid untuk dekripsi")
                return
        
        result.extend([chr(int(v) + ord('A')) for v in encrypted_vector])
    
    return ''.join(result)

class EncryptionApp:
    def __init__(self, master):
        self.master = master
        master.title("Aplikasi Enkripsi")
        master.geometry("600x400")

        self.label_text = ttk.Label(master, text="Teks:")
        self.label_text.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        
        self.text_input = tk.Text(master, height=5)
        self.text_input.grid(row=1, column=0, columnspan=3, padx=5, pady=5, sticky="nsew")

        self.label_key = ttk.Label(master, text="Kunci (min. 12 karakter):")
        self.label_key.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        
        self.key_input = ttk.Entry(master)
        self.key_input.grid(row=2, column=1, columnspan=2, padx=5, pady=5, sticky="ew")

        self.label_cipher = ttk.Label(master, text="Pilih Cipher:")
        self.label_cipher.grid(row=3, column=0, padx=5, pady=5, sticky="w")
        
        self.cipher_choice = ttk.Combobox(master, values=["Vigenere", "Playfair", "Hill"])
        self.cipher_choice.grid(row=3, column=1, columnspan=2, padx=5, pady=5, sticky="ew")
        self.cipher_choice.set("Vigenere")

        self.encrypt_button = ttk.Button(master, text="Enkripsi", command=lambda: self.process_text('encrypt'))
        self.encrypt_button.grid(row=4, column=0, padx=5, pady=5)

        self.decrypt_button = ttk.Button(master, text="Dekripsi", command=lambda: self.process_text('decrypt'))
        self.decrypt_button.grid(row=4, column=1, padx=5, pady=5)

        self.load_file_button = ttk.Button(master, text="Muat File", command=self.load_file)
        self.load_file_button.grid(row=4, column=2, padx=5, pady=5)

        self.result_label = ttk.Label(master, text="Hasil:")
        self.result_label.grid(row=5, column=0, padx=5, pady=5, sticky="w")

        self.result_text = tk.Text(master, height=5)
        self.result_text.grid(row=6, column=0, columnspan=3, padx=5, pady=5, sticky="nsew")

        master.columnconfigure(0, weight=1)
        master.columnconfigure(1, weight=1)
        master.columnconfigure(2, weight=1)
        master.rowconfigure(1, weight=1)
        master.rowconfigure(6, weight=1)

    def process_text(self, mode):
        text = self.text_input.get("1.0", tk.END).strip()
        key = self.key_input.get()
        cipher = self.cipher_choice.get().lower()

        if len(key) < 12:
            messagebox.showerror("Error", "Panjang kunci minimal 12 karakter")
            return

        if cipher == 'vigenere':
            result = vigenere_cipher(text, key, mode)
        elif cipher == 'playfair':
            result = playfair_cipher(text, key, mode)
        elif cipher == 'hill':
            result = hill_cipher(text, key, mode)
        else:
            messagebox.showerror("Error", "Cipher tidak valid")
            return

        self.result_text.delete("1.0", tk.END)
        self.result_text.insert(tk.END, result)

    def load_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, 'r') as file:
                content = file.read()
                self.text_input.delete("1.0", tk.END)
                self.text_input.insert(tk.END, content)

if __name__ == '__main__':
    root = tk.Tk()
    app = EncryptionApp(root)
    root.mainloop()
