# Program Cipher Encryption

Aplikasi ini mengimplementasikan tiga algoritma enkripsi:
1. Vigenere Cipher
2. Playfair Cipher
3. Hill Cipher

## Cara Menjalankan Program

### Langkah-langkah:
1. Pastikan Anda sudah menginstall Python di komputer Anda.
2. Install library `numpy` dan `tkinter` jika belum terinstall. Gunakan perintah berikut di terminal:
   >> pip install numpy
3. Buka terminal atau command prompt, navigasikan ke direktori tempat file program ini berada.
   >> cd path/to/your/program
4. Jalankan program dengan perintah:
   >> python encryption_app.py
5. Sebuah GUI akan muncul. Anda dapat memasukkan teks yang ingin dienkripsi atau didekripsi, serta memilih metode cipher yang diinginkan (Vigenere, Playfair, atau Hill).
6. Pastikan kunci yang dimasukkan memiliki panjang minimal 12 karakter.
7. Anda juga bisa memuat teks dari file `.txt` menggunakan fitur "Muat File".
8. Setelah proses enkripsi atau dekripsi, hasil akan ditampilkan di bagian bawah.

### Catatan:
- Pastikan kunci untuk Hill Cipher adalah string dengan panjang 9 karakter (misalnya "ABCDEFHIJ") untuk membentuk matriks 3x3.
- Untuk Vigenere dan Playfair Cipher, gunakan kunci minimal 12 karakter.

## Dependencies:
- Python 3.x
- numpy
- tkinter (sudah terinstall di Python untuk sistem operasi Windows dan macOS secara default)
