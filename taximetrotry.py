import time

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
        print("Carrera iniciada")

    def finalizar_carrera(self):
        if self.movimiento:
            self.movimiento = False
            self._update_precio()
            print(f"Carrera finalizada, su precio total es: {self.precio_total: .2f}euros")
        else:
            print("No hay ninguna carrera en curso.")

    def pausar_carrera(self):
        if self.movimiento:
            self._update_precio()
            self.running = False
            print("Taxi en espera")
        else:
            print("El Taxi esta en espera")
    
    def reanudar_carrera(self):
        if not self.movimiento:
            self.tiempo_inicio = time.time()
            self.movimiento = True
            print("Taxi en movimiento")
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

def main():
    taximetro = Taximetro()
    print("Bienvenid@ al tu calculador de tárifas para taxi")
    print("Tus comandos disponibles son: inicio, parar, pausa, continuar, salir")

    while True:
        command = input("Ingrese un comando: ").strip().lower()
        if command == "inicio":
            taximetro.comenzar_carrera()
        elif command == "parar":
            taximetro.finalizar_carrera()
        elif command == "pausar":
            taximetro.pausar_carrera()
        elif command == "continuar":
            taximetro.reanudar_carrera()
        elif command == "salir":
            print("Salienndo del calculador.")
            break
        else:
            print("Comando no válido, vuelve a intentarlo")

if __name__ == "__main__":
    taximetro = Taximetro()
    taximetro.comenzar_carrera()