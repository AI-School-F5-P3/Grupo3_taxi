# Pregunta al principio si queremos cambiar la tarifa para cumplir con 4º requisito del nivel medio
import time

class Taximetro:
    def __init__(self):
        self.tarifa_parado = 0.02
        self.tarifa_movimiento = 0.05
        self.tiempo_total = 0
        self.total_euros = 0
        self.en_movimiento = False
        self.tiempo_ultimo_cambio = time.time()
        self.tiempo_parado = 0
        self.tiempo_movimiento = 0

    def iniciar_carrera(self):
        self.configurar_tarifas()
        while True:
            print("Bienvenido al taxímetro digital. La carrera ha comenzado.")
            print("Instrucciones:")
            print("- Para indicar que el taxi está en movimiento, escribe 'marcha'.")
            print("- Para indicar que el taxi se detiene, escribe 'parada'.")
            print("- Para finalizar la carrera, escribe 'fin'.")
            print("- Para configurar tarifas, escribe '0.0x 0.0x'\n Donde primer parametro tarifa parado y segundo - tarifa movimiento.")
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
                else:
                    print("Instrucción no válida. Inténtalo de nuevo.")

            continuar = input("¿Desea iniciar una nueva carrera? (s/n): ").strip().lower()
            if continuar == 's':
                self.resetear_valores()
                self.configurar_tarifas()
            elif continuar == 'n':
                break
            else:
                print("Instrucción no válida. Inténtalo de nuevo.")

    def configurar_tarifas(self):
        cambiar_tarifas = input("¿Quieres cambiar la tarifa original? (sí/no): ").strip().lower()
        if cambiar_tarifas == 'sí' or cambiar_tarifas == 'si':
            try:
                nueva_tarifa_parado = float(input("Introduce la nueva tarifa en parada (€/minuto): "))
                nueva_tarifa_movimiento = float(input("Introduce la nueva tarifa en movimiento (€/minuto): "))
                self.tarifa_parado = nueva_tarifa_parado
                self.tarifa_movimiento = nueva_tarifa_movimiento
                print("Tarifas actualizadas.")
            except ValueError:
                print("Error: Introduce valores numéricos válidos.")
                self.configurar_tarifas()  # Volver a preguntar si hay un error
        else:
            print("Se mantienen las tarifas por defecto.")

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

    def resetear_valores(self):
        self.tiempo_total = 0
        self.total_euros = 0
        self.en_movimiento = False
        self.tiempo_ultimo_cambio = time.time()
        self.tiempo_parado = 0
        self.tiempo_movimiento = 0

if __name__ == "__main__":
    taximetro = Taximetro()
    taximetro.iniciar_carrera()
