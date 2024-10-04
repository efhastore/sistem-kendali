import serial  # Memasukkan library serial untuk komunikasi dengan Arduino
import tkinter as tk  # Memasukkan library tkinter untuk tampilan jendela GUI
from tkinter import messagebox  # Mengimpor messagebox untuk menampilkan popup konfirmasi saat keluar

# Inisialisasi komunikasi Serial
ser = serial.Serial('COM8', 9600, timeout=1)  # Sesuaikan port dengan Arduino Anda

# Fungsi untuk mengirim perintah ke Arduino
def send_command(command):
    ser.write(command.encode())  # Mengonversi string perintah menjadi bytes dan mengirimkannya ke Arduino
    ser.flush()  # Mengosongkan buffer output, memastikan semua data dikirim

# Fungsi untuk memilih mode otomatis
def set_automatic_mode():
    send_command('mode otomatis\n')  # Mengirim perintah untuk mengubah mode ke otomatis
    status_label.config(text="Mode: Otomatis")  # Memperbarui label status GUI
    manual_frame.pack_forget()  # Menghilangkan frame kontrol manual dari tampilan

# Fungsi untuk memilih mode manual
def set_manual_mode():
    send_command('mode manual\n')  # Mengirim perintah untuk mengubah mode ke manual
    status_label.config(text="Mode: Manual")  # Memperbarui label status GUI
    manual_frame.pack()  # Menampilkan frame kontrol manual

# Fungsi untuk menyalakan LED (manual)
def turn_on_led():
    send_command('ON\n')  # Mengirim perintah untuk menyalakan LED
    status_label.config(text="LED: ON (Manual)")  # Memperbarui label status GUI

# Fungsi untuk mematikan LED (manual)
def turn_off_led():
    send_command('OFF\n')  # Mengirim perintah untuk mematikan LED
    status_label.config(text="LED: OFF (Manual)")  # Memperbarui label status GUI

# Fungsi untuk menutup jendela dengan aman
def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):  # Menanyakan konfirmasi keluar
        ser.close()  # Menutup port serial sebelum keluar
        root.destroy()  # Menghentikan program dan menutup jendela GUI

# Membuat jendela Tkinter
root = tk.Tk()  # Membuat objek jendela utama Tkinter
root.title("Arduino Control")  # Mengatur judul jendela

# Label Status
status_label = tk.Label(root, text="Mode: Sistem Mati", font=("Arial", 12))  # Menampilkan status awal kosong
status_label.pack(pady=10)  # Menampilkan label dengan jarak vertikal

# Tombol untuk memilih mode
auto_button = tk.Button(root, text="Mode Otomatis", command=set_automatic_mode, width=20)  # Tombol untuk mode otomatis
auto_button.pack(pady=5)  # Menampilkan tombol dengan jarak vertikal

manual_button = tk.Button(root, text="Mode Manual", command=set_manual_mode, width=20)  # Tombol untuk mode manual
manual_button.pack(pady=5)  # Menampilkan tombol dengan jarak vertikal

# Frame untuk kontrol manual
manual_frame = tk.Frame(root)  # Membuat frame untuk menampung tombol kontrol manual

# Tombol manual untuk ON/OFF LED
on_button = tk.Button(manual_frame, text="Turn ON", command=turn_on_led, width=15)  # Tombol untuk menyalakan LED
on_button.grid(row=0, column=0, padx=10)  # Menampilkan tombol di grid dengan padding horizontal

off_button = tk.Button(manual_frame, text="Turn OFF", command=turn_off_led, width=15)  # Tombol untuk mematikan LED
off_button.grid(row=0, column=1, padx=10)  # Menampilkan tombol di grid dengan padding horizontal

# Event untuk menutup aplikasi dengan aman
root.protocol("WM_DELETE_WINDOW", on_closing)  # Mengatur protokol untuk menutup jendela

# Memulai loop Tkinter
root.mainloop()  # Memulai loop utama GUI untuk menangani interaksi pengguna
