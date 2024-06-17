import time
import logging
import tkinter as tk
from tkinter import simpledialog
from tkinter import messagebox
import hashlib

logging.basicConfig(filename = 'taximetro.log', level=logging.INFO, format='%(asctime)s - %(message)s')

class Taximetro:
    def __init__(self):
        self.movimiento = False
        self.precio_total = 0.0
        self.tiempo_inicio = None
        self.tiempo_espera = 0
        self.precio_por_minuto_movimiento = 0.5
        self.precio_por_minuto_espera = 0.2
        self.historial_file = 'taxi_history1.txt'

    def comenzar_carrera(self):
        self.movimiento = True
        self.precio_total = 0.0
        self.tiempo_inicio = time.time()
        logging.info("Carrera iniciada")
        print("Carrera iniciada")

    def finalizar_carrera(self):
        if self.movimiento:
            self.movimiento = False
            self._update_precio()
            logging.info(f"Carrera finalizada, su precio total es: {self.precio_total:.2f} euros")
            with open(self.historial_file, 'a') as f:
                f.write(f"Carrera finalizada, su precio total es: {self.precio_total:.2f} euros\n")
            print(f"Carrera finalizada, su precio total es: {self.precio_total:.2f} euros")
        else:
            print("No hay ninguna carrera en curso.")

    def pausar_carrera(self):
        if self.movimiento:
            self._update_precio()
            self.running = False
            logging.info("Taxi en espera.")
            print("Taxi en espera")
        else:
            print("El Taxi esta en espera")
    
    def reanudar_carrera(self):
        if not self.movimiento:
            self.tiempo_inicio = time.time()
            self.movimiento = True
            logging.info("Taxi en movimiento.")
            print("Taxi en movimiento.")
        else:
            print("El Taxi ya esta en movimiento")

    def _update_precio(self):
        if self.tiempo_inicio:
            tiempo_transcurrido = time.time() - self.tiempo_inicio
            if self.movimiento:
                self.precio_total += tiempo_transcurrido / 60 * self.precio_por_minuto_movimiento
            else:
                self.precio_total += tiempo_transcurrido / 60 * self.precio_por_minuto_espera
            self.tiempo_inicio = time.time()
class Password:
    def __init__(self):
        self.datos_usuario = {}
        self.load_datos_usuario()
    
    def load_datos_usuario(self):
        try:
            with open('datos_usuario.txt', 'r') as file:
                for line in file:
                    usuario, hashed_password = line.strip().split(',')
                    self.datos_usuario[usuario] = hashed_password
        except FileNotFoundError:
            pass
    
    def save_datos_usuario(self):
        with open('datos_usuario.txt', 'w') as file:
            for usuario, hashed_password in self.datos_usuario.items():
                file.write(f'{usuario},{hashed_password}\n')
    
    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()
    
    def register(self, nombre_usuario, password):
        if nombre_usuario in self.datos_usuario:
            raise ValueError("Usuario ya registrado.")
        self.datos_usuario[nombre_usuario] = self.hash_password(password)
        self.save_datos_usuario()

    def authenticate(self, nombre_usuario, password):
        hashed_password = self.hash_password(password)
        return self.datos_usuario.get(nombre_usuario) == hashed_password

    
class TarifaTaxi:
    def __init__(self, master, auth):
        self.master = master
        self.auth = auth
        self.taximetro = Taximetro()

        self.master.title("Taximetro")
        self.master.geometry("300x200")

        self.auth_frame = tk.Frame(master)
        self.auth_frame.pack()

        self.user_label = tk.Label(self.auth_frame, text="Usuario")
        self.user_label.pack(pady=5)

        self.user_entry = tk.Entry(self.auth_frame)
        self.user_entry.pack(pady=5)

        self.password_label = tk.Label(self.auth_frame, text="Contraseña")
        self.password_label.pack(pady=5)

        self.password_entry = tk.Entry(self.auth_frame, show="*")
        self.password_entry.pack(pady=5)

        self.login_button = tk.Button(self.auth_frame, text="Iniciar Sesión", command=self.login)
        self.login_button.pack(pady=5)

        self.register_button = tk.Button(self.auth_frame, text="Registrarse", command=self.register)
        self.register_button.pack(pady=5)

        self.taxi_frame = tk.Frame(master)

    def login(self):
        nombre_usuario = self.user_entry.get()
        password = self.password_entry.get()
        if self.auth.authenticate(nombre_usuario, password):
            self.auth_frame.pack_forget()
            self.taxi_frame.pack()
            self.create_taxi_interface()
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")

    def register(self):
        nombre_usuario = self.user_entry.get()
        password = self.password_entry.get()
        try:
            self.auth.register(nombre_usuario, password)
            messagebox.showinfo("Éxito", "Usuario registrado correctamente")
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def create_taxi_interface(self):
        self.start_button = tk.Button(self.taxi_frame, text="Iniciar", command=self.start_trip)
        self.start_button.pack(pady=10)

        self.stop_button = tk.Button(self.taxi_frame, text="Parar", command=self.stop_trip)
        self.stop_button.pack(pady=10)

        self.pause_button = tk.Button(self.taxi_frame, text="Pausar", command=self.pause_trip)
        self.pause_button.pack(pady=10)

        self.resume_button = tk.Button(self.taxi_frame, text="Continuar", command=self.resume_trip)
        self.resume_button.pack(pady=10)

    def comenzar_carrera(self):
        self.taximetro.start_trip()

    def finalizar_carrera(self):
        self.taximetro.stop_trip()

    def pausar_carrera(self):
        self.taximetro.pause_trip()

    def reaudar_carrera(self):
        self.taximetro.resume_trip()

if __name__ == "__main__":
    root = tk.Tk()
    auth = Password()
    app = TarifaTaxi(root, auth)
    root.mainloop()