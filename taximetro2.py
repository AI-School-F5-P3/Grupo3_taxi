import time

class Taximetro:
    def __init__(self):
        self.tarifa_parado = 0.02  # Tarifa por segundo cuando el taxi está parado
        self.tarifa_movimiento = 0.05  # Tarifa por segundo cuando el taxi está en movimiento
        self.tiempo_total = 0  # Tiempo total de la carrera en segundos
        self.total_euros = 0  # Total a cobrar en euros
        self.tiempo_inicio = None

    def iniciar_carrera(self):
        print("Bienvenido al taxímetro digital. La carrera ha comenzado.")
        print("Instrucciones:")
        print("- Para indicar que el taxi está en movimiento, escribe 'marcha'.")
        print("- Para indicar que el taxi se detiene, escribe 'parada'.")
        print("- Para finalizar la carrera, escribe 'fin'.")
        print()

        self.tiempo_inicio = time.time()

        while True:
            instruccion = input("Esperando instrucciones: ")
            if instruccion == "marcha":
                self.calcular_tarifa_movimiento()
            elif instruccion == "parada":
                self.calcular_tarifa_parado()
            elif instruccion == "fin":
                self.finalizar_carrera()
                break
            else:
                print("Instrucción no válida. Inténtalo de nuevo.")

    def calcular_tarifa_movimiento(self):
        tiempo_actual = time.time()
        tiempo_transcurrido = tiempo_actual - self.tiempo_inicio
        self.tiempo_total += tiempo_transcurrido
        self.total_euros += tiempo_transcurrido * self.tarifa_movimiento
        self.tiempo_inicio = tiempo_actual

    def calcular_tarifa_parado(self):
        tiempo_actual = time.time()
        tiempo_transcurrido = tiempo_actual - self.tiempo_inicio
        self.tiempo_total += tiempo_transcurrido
        self.total_euros += tiempo_transcurrido * self.tarifa_parado
        self.tiempo_inicio = tiempo_actual

    def finalizar_carrera(self):
        # Muestra el total a cobrar
        print(f"Total a cobrar: {self.total_euros:.2f} euros")

        # Reinicia los valores para una nueva carrera
        self.tiempo_total = 0
        self.total_euros = 0
        self.tiempo_inicio = None

if __name__ == "__main__":
    taximetro = Taximetro()
    taximetro.iniciar_carrera()
