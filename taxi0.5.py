import time
import logging
import argparse

# Configuración del sistema de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', handlers=[
    logging.FileHandler("taximetro.log"),  # Archivo de registro
    logging.StreamHandler()  # Salida en consola
])

class Taximetro:
    def __init__(self, password):
        self.tarifa_parado = 0.02
        self.tarifa_movimiento = 0.05
        self.tiempo_total = 0
        self.total_euros = 0
        self.en_movimiento = False
        self.tiempo_ultimo_cambio = time.time()
        self.tiempo_parado = 0
        self.tiempo_movimiento = 0
        self.password = password  # Contraseña para configurar tarifas
        self.autenticado = False  # Bandera para saber si ya se ha autenticado
        logging.info("Taxímetro iniciado con tarifas por defecto y contraseña establecida.")

    def iniciar_carrera(self):
        self.autenticar()
        self.configurar_tarifas()
        while True:
            logging.info("Nueva carrera iniciada.")
            print("Bienvenido al taxímetro digital. La carrera ha comenzado.")
            print("Instrucciones:")
            print("- Para indicar que el taxi está en movimiento, escribe 'marcha'.")
            print("- Para indicar que el taxi se detiene, escribe 'parada'.")
            print("- Para finalizar la carrera, escribe 'fin'.")
            print("- Para configurar tarifas, escribe 'configurar'.")
            print()

            self._cambiar_estado(time.time(), False)

            while True:
                instruccion = input("Esperando instrucciones: ").strip().lower()
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
                else:
                    print("Instrucción no válida. Inténtalo de nuevo.")
                    logging.warning("Instrucción no válida recibida: %s", instruccion)

            continuar = input("¿Desea iniciar una nueva carrera? (s/n): ").strip().lower()
            if continuar == 's':
                self.resetear_valores()
                self.configurar_tarifas()
            elif continuar == 'n':
                break
            else:
                print("Instrucción no válida. Inténtalo de nuevo.")
                logging.warning("Instrucción no válida para continuar: %s", continuar)

    def autenticar(self):
        intentos = 3
        while intentos > 0:
            if not self.autenticado:
                contraseña_ingresada = input("Ingresa la contraseña para continuar: ").strip()
                if contraseña_ingresada == self.password:
                    self.autenticado = True
                    logging.info("Contraseña correcta. Acceso concedido.")
                else:
                    print("Contraseña incorrecta. Inténtalo de nuevo.")
                    logging.warning("Intento de acceso con contraseña incorrecta.")
                    intentos -= 1
            else:
                break

        if intentos == 0:
            logging.error("Número máximo de intentos alcanzado. Cierre del programa.")
            print("Número máximo de intentos alcanzado. Cierre del programa.")
            exit()  # Salir del programa si se superan los intentos máximos

    def configurar_tarifas(self):
        if not self.autenticado:
            logging.warning("No se ha autenticado. Debes autenticarte para configurar las tarifas.")
            return

        try:
            nueva_tarifa_parado = float(input("Introduce la nueva tarifa en parada (€/minuto): "))
            nueva_tarifa_movimiento = float(input("Introduce la nueva tarifa en movimiento (€/minuto): "))
            self.tarifa_parado = nueva_tarifa_parado
            self.tarifa_movimiento = nueva_tarifa_movimiento
            logging.info("Tarifas actualizadas a parada: %.2f, movimiento: %.2f", self.tarifa_parado, self.tarifa_movimiento)
            print("Tarifas actualizadas.")
        except ValueError:
            logging.error("Error al introducir tarifas. Valores no numéricos.")
            print("Error: Introduce valores numéricos válidos.")

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
        print(f"Total a cobrar: {self.total_euros:.2f} euros")

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
    parser.add_argument('--password', type=str, default='1234', help='Contraseña para configurar tarifas (por defecto: "1234")')
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    taximetro = Taximetro(password=args.password)
    taximetro.iniciar_carrera()
