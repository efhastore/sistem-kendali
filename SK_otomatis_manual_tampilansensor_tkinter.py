import serial  # Memasukkan library serial
import tkinter as tk  # Memasukkan library tkinter / tampilan jendela 
from tkinter import messagebox  # Menampilkan popup untuk exit

# Inisialisasi komunikasi Serial (sesuaikan COM port sesuai dengan Arduino)
ser = serial.Serial('COM8', 9600, timeout=1)

# Fungsi untuk mengirim perintah ke Arduino
def send_command(command):
    ser.write(command.encode())  # Mengonversi string perintah menjadi bytes
    ser.flush()  # Mengosongkan buffer output

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
        ser.close()  # Menutup port serial saat keluar
        root.destroy()  # Menghentikan program dan menutup jendela GUI

# Fungsi untuk membaca data sensor dari Arduino
def read_sensor_data():
    if ser.in_waiting > 0:  # Memeriksa apakah ada data yang tersedia untuk dibaca
        try:
            line = ser.readline().decode('utf-8').strip()  # Membaca dan mendekode data
            if "Lux =" in line:  # Memeriksa format data
                sensor_value_label.config(text=f"Sensor: {line}")  # Memperbarui label data sensor
        except:
            pass  # Jika terjadi kesalahan, abaikan
    root.after(1000, read_sensor_data)  # Membaca data sensor setiap 1 detik

# Membuat jendela Tkinter
root = tk.Tk()  # Membuat objek jendela utama Tkinter
root.title("Arduino Control")  # Mengatur judul jendela

# Label Status
status_label = tk.Label(root, text="Mode: Sistem Mati", font=("Arial", 12))  # Menampilkan status awal kosong
status_label.pack(pady=10)  # Menampilkan label dengan jarak vertikal

# Label Sensor Data
sensor_value_label = tk.Label(root, text="Sensor: --", font=("Arial", 12))  # Label untuk data sensor
sensor_value_label.pack(pady=10)  # Menampilkan label dengan jarak vertikal

# Tombol untuk memilih mode
auto_button = tk.Button(root, text="Mode Otomatis", command=set_automatic_mode, width=20)  # Tombol untuk mode otomatis
auto_button.pack(pady=5)  # Menampilkan tombol dengan jarak vertikal

manual_button = tk.Button(root, text="Mode Manual", command=set_manual_mode, width=20)  # Tombol untuk mode manual
manual_button.pack(pady=5)  # Menampilkan tombol dengan jarak vertikal

# Frame untuk kontrol manual
manual_frame = tk.Frame(root)  # Membuat frame untuk menampung tombol kontrol manual
# Kontrol manual hanya akan ditampilkan jika mode manual dipilih

# Tombol manual untuk ON/OFF LED
on_button = tk.Button(manual_frame, text="Turn ON", command=turn_on_led, width=15)  # Tombol untuk menyalakan LED
on_button.grid(row=0, column=0, padx=10)  # Menampilkan tombol di grid dengan padding horizontal

off_button = tk.Button(manual_frame, text="Turn OFF", command=turn_off_led, width=15)  # Tombol untuk mematikan LED
off_button.grid(row=0, column=1, padx=10)  # Menampilkan tombol di grid dengan padding horizontal

# Event untuk menutup aplikasi dengan aman
root.protocol("WM_DELETE_WINDOW", on_closing)  # Mengatur protokol untuk menutup jendela

# Mulai membaca data sensor dari Arduino
read_sensor_data()  # Memulai fungsi membaca data sensor

# Memulai loop Tkinter
root.mainloop()  # Memulai loop utama GUI untuk menangani interaksi pengguna
