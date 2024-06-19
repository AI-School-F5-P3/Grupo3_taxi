# corregido el fallo de volver a empezar la carrera cuando al finalizar contestamos que queremos una nueva carrera
import time
import logging
import argparse
import tkinter as tk
from tkinter import messagebox, simpledialog
import sqlite3
from PIL import Image, ImageTk

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', handlers=[
    logging.FileHandler("taximetro.log"),
    logging.StreamHandler()
])

class Taximetro:
    def __init__(self, contraseña):
        self.tarifa_parado = 0.02
        self.tarifa_movimiento = 0.05
        self.tiempo_total = 0
        self.total_euros = 0
        self.en_movimiento = False
        self.tiempo_ultimo_cambio = time.time()
        self.tiempo_parado = 0
        self.tiempo_movimiento = 0
        self.contraseña = contraseña
        self.autenticado = False
        self.conexion_bd = None
        self.crear_tabla_registros()
        logging.info("Taxímetro iniciado con tarifas por defecto y contraseña establecida.")

    def iniciar_carrera(self, root):
        self.autenticar(root)
        if not self.autenticado:
            return

        self.root = root
        self.root.title("Taxímetro Digital")
        self.root.geometry("430x550")
        self.root.configure(bg="black")
        
        # Load and display the image
        try:
            image = Image.open("taximide_vertical_logo.png")  # Ruta relativa al archivo de imagen
            image = image.resize((250, 100), Image.LANCZOS)  # Resize the image if needed
            self.image_tk = ImageTk.PhotoImage(image)
            self.image_label = tk.Label(root, image=self.image_tk, bg="black")
            self.image_label.pack(pady=10)
        except FileNotFoundError:
            logging.error("El archivo de imagen no se encuentra. Asegúrate de que 'taximide_logo.png' está en el mismo directorio que tu script de Python.")
            messagebox.showerror("Error", "El archivo de imagen no se encuentra. Asegúrate de que 'taximide_logo.png' está en el mismo directorio que tu script de Python.")

        self.estado_label = tk.Label(root, text="Taxi en parado.", font=("Helvetica", 20), fg="white", bg="black")
        self.estado_label.pack(pady=10)

        self.tarifa_parado_label = tk.Label(root, text=f"Tarifa en parado: {self.tarifa_parado:.2f} €/minuto", font=("Helvetica", 16), fg="white", bg="black")
        self.tarifa_parado_label.pack()

        self.tarifa_movimiento_label = tk.Label(root, text=f"Tarifa en movimiento: {self.tarifa_movimiento:.2f} €/minuto", font=("Helvetica", 16), fg="white", bg="black")
        self.tarifa_movimiento_label.pack(pady=10)

        # Creamos un Canvas para los contadores visuales
        self.canvas_tiempo = tk.Canvas(root, width=300, height=50, bg="grey", highlightthickness=5)
        self.canvas_tiempo.pack(pady=10)

        self.canvas_euros = tk.Canvas(root, width=300, height=50, bg="grey", highlightthickness=5)
        self.canvas_euros.pack(pady=10)

        button_frame = tk.Frame(root, bg="black")
        button_frame.pack(pady=10)

        self.boton_marcha = tk.Button(button_frame, text="Marcha", font=("Helvetica", 14, "bold"), command=self.iniciar_movimiento, width=12, bg="white", fg="black")
        self.boton_marcha.grid(row=0, column=0, padx=5, pady=5)

        self.boton_parada = tk.Button(button_frame, text="Parada", font=("Helvetica", 14, "bold"), command=self.detener_movimiento, width=12, bg="white", fg="black")
        self.boton_parada.grid(row=0, column=1, padx=5)

        self.boton_fin = tk.Button(button_frame, text="Fin", font=("Helvetica", 14, "bold"), command=self.finalizar_carrera, width=12, bg="white", fg="black")
        self.boton_fin.grid(row=1, column=0, padx=5, pady=5)

        self.boton_configurar = tk.Button(button_frame, text="Configurar tarifas", font=("Helvetica", 14, "bold"), command=self.configurar_tarifas, width=18, bg="white", fg="black")
        self.boton_configurar.grid(row=1, column=1, padx=5, pady=5)

        self.boton_cambiar_contraseña = tk.Button(button_frame, text="Cambiar contraseña", font=("Helvetica", 14, "bold"), command=self.cambiar_contraseña, width=18, bg="white", fg="black")
        self.boton_cambiar_contraseña.grid(row=2, column=0, columnspan=2, pady=5)

        self.actualizar_tiempo_costo()

    def actualizar_tiempo_costo(self):
        tiempo_actual = time.time()
        tiempo_transcurrido = tiempo_actual - self.tiempo_ultimo_cambio
        if self.en_movimiento:
            self.tiempo_movimiento += tiempo_transcurrido
        else:
            self.tiempo_parado += tiempo_transcurrido
        
        self.tiempo_total = self.tiempo_movimiento + self.tiempo_parado
        self.total_euros = (self.tiempo_movimiento * self.tarifa_movimiento) + (self.tiempo_parado * self.tarifa_parado)

        horas, resto = divmod(self.tiempo_total, 3600)
        minutos, segundos = divmod(resto, 60)
        tiempo_formateado = f"⌚️ {int(horas):02}:{int(minutos):02}:{int(segundos):02}"

        # Actualizamos los contadores visuales en el Canvas
        self.actualizar_canvas(self.canvas_tiempo, tiempo_formateado)
        self.actualizar_canvas(self.canvas_euros, f"{self.total_euros:.2f} €")

        self.tiempo_ultimo_cambio = tiempo_actual
        self.root.after(1000, self.actualizar_tiempo_costo)

    def actualizar_canvas(self, canvas, texto):
        canvas.delete("all")  # Borramos todo lo dibujado previamente en el Canvas
        canvas.create_text(150, 30, text=texto, font=("Arial", 38), fill="white")

    def autenticar(self, root):
        if not self.autenticado:
            contraseña_ingresada = simpledialog.askstring("Autenticación", "Ingresa la contraseña para continuar:", show='*')
            if contraseña_ingresada == self.contraseña:
                self.autenticado = True
                logging.info("Contraseña correcta. Acceso concedido.")
            else:
                messagebox.showerror("Error", "Contraseña incorrecta. Cierre del programa.")
                logging.warning("Intento de acceso con contraseña incorrecta.")
                root.destroy()

    def crear_tabla_registros(self):
        try:
            self.conexion_bd = sqlite3.connect("registros.db")
            cursor = self.conexion_bd.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS registros (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    tiempo_inicio TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    tiempo_fin TIMESTAMP,
                    tiempo_parado REAL,
                    tiempo_movimiento REAL,
                    total_euros REAL
                )
            ''')
            self.conexion_bd.commit()
            logging.info("Tabla 'registros' creada correctamente.")
        except sqlite3.Error as e:
            logging.error(f"Error al crear la tabla 'registros': {e}")

    def insertar_registro(self, tiempo_inicio, tiempo_fin, tiempo_parado, tiempo_movimiento, total_euros):
        try:
            cursor = self.conexion_bd.cursor()
            cursor.execute('''
                INSERT INTO registros (tiempo_inicio, tiempo_fin, tiempo_parado, tiempo_movimiento, total_euros)
                VALUES (?, ?, ?, ?, ?)
            ''', (tiempo_inicio, tiempo_fin, tiempo_parado, tiempo_movimiento, total_euros))
            self.conexion_bd.commit()
            logging.info("Registro insertado correctamente en la tabla 'registros'.")
        except sqlite3.Error as e:
            logging.error(f"Error al insertar registro en la tabla 'registros': {e}")

    def configurar_tarifas(self):
        if not self.autenticado:
            logging.warning("No se ha autenticado. Debes autenticarte para configurar las tarifas.")
            messagebox.showerror("Error", "No se ha autenticado. Debes autenticarte para configurar las tarifas.")
            return
        
        try:
            nueva_tarifa_parado = float(simpledialog.askstring("Configurar tarifas", "Introduce la nueva tarifa en parado (€/minuto):"))
            nueva_tarifa_movimiento = float(simpledialog.askstring("Configurar tarifas", "Introduce la nueva tarifa en movimiento (€/minuto):"))
            if nueva_tarifa_parado >= 0 and nueva_tarifa_movimiento >= 0:
                self.tarifa_parado = nueva_tarifa_parado
                self.tarifa_movimiento = nueva_tarifa_movimiento
                logging.info("Tarifas actualizadas en parado: %.2f, y en movimiento: %.2f", self.tarifa_parado, self.tarifa_movimiento)
                self.tarifa_parado_label.config(text=f"Tarifa en parado: {self.tarifa_parado:.2f} €/minuto")
                self.tarifa_movimiento_label.config(text=f"Tarifa en movimiento: {self.tarifa_movimiento:.2f} €/minuto")
            else:
                logging.error("Error al configurar tarifas. Los valores deben ser números positivos.")
                messagebox.showerror("Error", "Valores no válidos para las tarifas. Inténtalo de nuevo con números positivos.")

        except ValueError:
            logging.error("Error al configurar tarifas. Valores no válidos.")
            messagebox.showerror("Error", "Valores no válidos para las tarifas. Inténtalo de nuevo.")

    def cambiar_contraseña(self):
        if not self.autenticado:
            logging.warning("No se ha autenticado. Debes autenticarte para cambiar la contraseña.")
            messagebox.showerror("Error", "No se ha autenticado. Debes autenticarte para cambiar la contraseña.")
            return

        nueva_contraseña = simpledialog.askstring("Cambiar contraseña", "Ingresa la nueva contraseña:")
        if nueva_contraseña:
            self.contraseña = nueva_contraseña
            logging.info("Contraseña cambiada exitosamente.")
            messagebox.showinfo("Éxito", "Contraseña cambiada exitosamente.")
        else:
            logging.info("No se ha proporcionado una nueva contraseña.")
            messagebox.showwarning("Advertencia", "No se ha proporcionado una nueva contraseña.")

    def iniciar_movimiento(self):
        if not self.autenticado:
            logging.warning("No se ha autenticado. Debes autenticarte para iniciar el movimiento.")
            messagebox.showerror("Error", "No se ha autenticado. Debes autenticarte para iniciar el movimiento.")
            return

        if not self.en_movimiento:
            self.en_movimiento = True
            self.estado_label.config(text="Taxi en movimiento.", fg="green")
            logging.info("Taxi en movimiento.")
        else:
            logging.warning("El taxi ya está en movimiento.")

    def detener_movimiento(self):
        if not self.autenticado:
            logging.warning("No se ha autenticado. Debes autenticarte para detener el movimiento.")
            messagebox.showerror("Error", "No se ha autenticado. Debes autenticarte para detener el movimiento.")
            return

        if self.en_movimiento:
            self.en_movimiento = False
            self.estado_label.config(text="Taxi en parado.", fg="red")
            logging.info("Taxi detenido.")
        else:
            logging.warning("El taxi ya está en parado.")

    def finalizar_carrera(self):
        if not self.autenticado:
            logging.warning("No se ha autenticado. Debes autenticarte para finalizar la carrera.")
            messagebox.showerror("Error", "No se ha autenticado. Debes autenticarte para finalizar la carrera.")
            return

        self.insertar_registro(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(self.tiempo_ultimo_cambio)),
                               time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),
                               self.tiempo_parado, self.tiempo_movimiento, self.total_euros)
        self.conexion_bd.close()
        logging.info("Registro de carrera finalizado y guardado en la base de datos.")
        
        if hasattr(self, 'estado_label'):
            self.estado_label.config(text="Taxi en parado.", fg="red")
        else:
            logging.warning("estado_label no está inicializado. No se puede actualizar el estado visual.")

        mensaje = f"Carrera finalizada. Total a cobrar: {self.total_euros:.2f} euros.\n\n¿Desea iniciar una nueva carrera?"
        if messagebox.askyesno("Carrera finalizada", mensaje):
            self.reiniciar_carrera()
        else:
            if hasattr(self, 'root') and hasattr(self.root, 'quit'):
                self.root.quit()

    def reiniciar_carrera(self):
        # Reiniciar todos los valores de la carrera
        self.tiempo_total = 0
        self.total_euros = 0
        self.en_movimiento = False
        self.tiempo_ultimo_cambio = time.time()
        self.tiempo_parado = 0
        self.tiempo_movimiento = 0

        if hasattr(self, 'estado_label'):
            self.estado_label.config(text="Taxi en parado.", fg="red")
        else:
            logging.warning("estado_label no está inicializado. No se puede actualizar el estado visual.")
        
        self.actualizar_canvas(self.canvas_tiempo, "Tiempo transcurrido: 00:00:00")
        self.actualizar_canvas(self.canvas_euros, "Total a cobrar: 0.00 euros")

        # Habilitar los botones para una nueva carrera
        self.boton_marcha.config(state=tk.NORMAL)
        self.boton_parada.config(state=tk.NORMAL)
        self.boton_fin.config(state=tk.NORMAL)

    def iniciar_nueva_carrera(self):
        if not self.autenticado:
            logging.warning("No se ha autenticado. Debes autenticarte para iniciar una nueva carrera.")
            messagebox.showerror("Error", "No se ha autenticado. Debes autenticarte para iniciar una nueva carrera.")
            return

        # Si hay una carrera en curso, preguntar si desea finalizarla
        if self.en_movimiento:
            if messagebox.askyesno("Finalizar carrera", "¿Desea finalizar la carrera actual antes de iniciar una nueva?"):
                self.finalizar_carrera()
            else:
                return

        # Iniciar una nueva carrera
        self.reiniciar_carrera()
        self.iniciar_carrera(self.root)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Taxímetro interactivo con GUI")
    parser.add_argument("--contraseña", default="1234", help="Contraseña para acceder al taxímetro")
    args = parser.parse_args()

    taximetro = Taximetro(args.contraseña)

    root = tk.Tk()
    taximetro.iniciar_carrera(root)
    root.mainloop()
