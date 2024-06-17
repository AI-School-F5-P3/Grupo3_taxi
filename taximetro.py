class Taximetro:
    def __init__(self):
        self.tarifa_parado = 0.02  # Tarifa por segundo cuando el taxi está parado
        self.tarifa_movimiento = 0.05  # Tarifa por segundo cuando el taxi está en movimiento
        self.tiempo_total = 0  # Tiempo total de la carrera en segundos
        self.total_euros = 0  # Total a cobrar en euros

    def iniciar_carrera(self):
        print("Bienvenido al taxímetro digital. La carrera ha comenzado.")
        print("Instrucciones:")
        print("- Para indicar que el taxi está en movimiento, escribe 'marcha'.")
        print("- Para indicar que el taxi se detiene, escribe 'parada'.")
        print("- Para finalizar la carrera, escribe 'fin'.")
        print()

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
        # Implementa el cálculo de la tarifa cuando el taxi está en movimiento
        self.tiempo_total += 1  # Simulación: incrementa el tiempo en 1 segundo

    def calcular_tarifa_parado(self):
        # Implementa el cálculo de la tarifa cuando el taxi está parado
        self.tiempo_total += 1  # Simulación: incrementa el tiempo en 1 segundo

    def finalizar_carrera(self):
        # Calcula el total en euros y muestra el resultado
        self.total_euros = self.tiempo_total * self.tarifa_parado
        print(f"Total a cobrar: {self.total_euros:.2f} euros")

        # Reinicia los valores para una nueva carrera
        self.tiempo_total = 0
        self.total_euros = 0

if __name__ == "__main__":
    taximetro = Taximetro()
    taximetro.iniciar_carrera()