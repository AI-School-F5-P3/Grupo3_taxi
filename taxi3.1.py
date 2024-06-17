import time
import logging
import argparse
import tkinter as tk
from tkinter import simpledialog
from tkinter import messagebox

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
        self.contraseña = "1234"
        self.autenticado = False
        logging.info("Taxímetro iniciado con tarifas por defecto y contraseña establecida.")

    def iniciar_carrera(self):
        self.autenticar()
        while True:
            logging.info("Nueva carrera iniciada.")
            messagebox.showinfo("Taxímetro", "Bienvenido al taxímetro digital. La carrera ha comenzado.")

            while True:
                instruccion = self.pedir_instruccion()
                tiempo_actual = time.time()

                if instruccion == "marcha":
                    self._cambiar_estado(tiempo_actual, True)
                elif instruccion == "parada":
                    self._cambiar_estado(tiempo_actual, False)
                elif instruccion == "fin":
                    self.finalizar_carrera(tiempo_actual)
                    break
                elif instruccion == "configurar":
                    self.configurar_tarifas()
                elif instruccion == "cambiar_contraseña":
                    self.cambiar_contraseña()

            continuar = messagebox.askyesno("Taxímetro", "¿Desea iniciar una nueva carrera?")
            if not continuar:
                break
            self.resetear_valores()

    def pedir_instruccion(self):
        root = tk.Tk()
        root.withdraw()
        instruccion = simpledialog.askstring("Taxímetro", "Esperando instrucciones:").strip().lower()
        return instruccion

    def autenticar(self):
        intentos = 3
        while intentos > 0:
            if not self.autenticado:
                contraseña_ingresada = simpledialog.askstring("Autenticación", "Ingresa la contraseña para continuar:", show='*')
                if contraseña_ingresada == self.contraseña:
                    self.autenticado = True
                    logging.info("Contraseña correcta. Acceso concedido.")
                else:
                    messagebox.showwarning("Autenticación", "Contraseña incorrecta. Inténtalo de nuevo.")
                    logging.warning("Intento de acceso con contraseña incorrecta.")
                    intentos -= 1
            else:
                break

        if intentos == 0:
            logging.error("Número máximo de intentos alcanzado. Cierre del programa.")
            messagebox.showerror("Autenticación", "Número máximo de intentos alcanzado. Cierre del programa.")
            exit()

    def configurar_tarifas(self):
        if not self.autenticado:
            logging.warning("No se ha autenticado. Debes autenticarte para configurar las tarifas.")
            messagebox.showwarning("Configuración de Tarifas", "Debes autenticarte para configurar las tarifas.")
            return

        try:
            nueva_tarifa_parado = simpledialog.askfloat("Configuración de Tarifas", "Introduce la nueva tarifa en parada (€/minuto):")
            nueva_tarifa_movimiento = simpledialog.askfloat("Configuración de Tarifas", "Introduce la nueva tarifa en movimiento (€/minuto):")
            self.tarifa_parado = nueva_tarifa_parado
            self.tarifa_movimiento = nueva_tarifa_movimiento
            logging.info("Tarifas actualizadas a parada: %.2f, movimiento: %.2f", self.tarifa_parado, self.tarifa_movimiento)
            messagebox.showinfo("Configuración de Tarifas", f"Tarifas actualizadas a parada: {self.tarifa_parado:.2f}, movimiento: {self.tarifa_movimiento:.2f}")
        except ValueError:
            logging.error("Error al introducir tarifas. Valores no numéricos.")
            messagebox.showerror("Error", "Error al introducir tarifas. Introduce valores numéricos válidos.")

    def cambiar_contraseña(self):
        if not self.autenticado:
            logging.warning("No se ha autenticado. Debes autenticarte para cambiar la contraseña.")
            messagebox.showwarning("Cambiar Contraseña", "Debes autenticarte para cambiar la contraseña.")
            return

        nueva_contraseña = simpledialog.askstring("Cambiar Contraseña", "Introduce la nueva contraseña:", show='*')
        confirmacion_contraseña = simpledialog.askstring("Cambiar Contraseña", "Confirma la nueva contraseña:", show='*')

        if nueva_contraseña == confirmacion_contraseña:
            self.contraseña = nueva_contraseña
            logging.info("Contraseña cambiada exitosamente.")
            messagebox.showinfo("Cambiar Contraseña", "Contraseña cambiada exitosamente.")
        else:
            logging.warning("La nueva contraseña no coincide con la confirmación.")
            messagebox.showwarning("Cambiar Contraseña", "La nueva contraseña no coincide con la confirmación.")

    def _cambiar_estado(self, tiempo_actual, en_movimiento):
        tiempo_transcurrido = tiempo_actual - self.tiempo_ultimo_cambio
        if self.en_movimiento:
            self.tiempo_movimiento += tiempo_transcurrido
        else:
            self.tiempo_parado += tiempo_transcurrido

        self.en_movimiento = en_movimiento
        self.tiempo_ultimo_cambio = tiempo_actual
        estado = "movimiento" if en_movimiento else "parado"
        print(f"Taxi en {estado}.")

    def finalizar_carrera(self, tiempo_actual):
        tiempo_transcurrido = tiempo_actual - self.tiempo_ultimo_cambio
        if self.en_movimiento:
            self.tiempo_movimiento += tiempo_transcurrido
        else:
            self.tiempo_parado += tiempo_transcurrido

        self.total_euros = (self.tiempo_movimiento * self.tarifa_movimiento) + (self.tiempo_parado * self.tarifa_parado)
        mensaje = f"Total a cobrar: {self.total_euros:.2f} euros"
        logging.info(mensaje)
        messagebox.showinfo("Finalizar Carrera", mensaje)

        self.resetear_valores()

    def resetear_valores(self):
        self.tiempo_total = 0
        self.total_euros = 0
        self.en_movimiento = False
        self.tiempo_ultimo_cambio = time.time()
        self.tiempo_parado = 0
        self.tiempo_movimiento = 0

def parse_args():
    parser = argparse.ArgumentParser(description='Taxímetro digital - Aplicación CLI')
    parser.add_argument('--contraseña', type=str, default='1234', help='Contraseña para configurar tarifas (por defecto: "1234")')
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    taximetro = Taximetro(contraseña=args.contraseña)
    taximetro.iniciar_carrera()
