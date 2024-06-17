import unittest
from unittest.mock import patch
import time
from taximetro6 import Taximetro

class TestTaximetro(unittest.TestCase):

    def setUp(self):
        self.taximetro = Taximetro()

    @patch('builtins.input', side_effect=['no'])
    def test_configurar_tarifas_por_defecto(self, mock_input):
        self.taximetro.configurar_tarifas()
        self.assertEqual(self.taximetro.tarifa_parado, 0.02)
        self.assertEqual(self.taximetro.tarifa_movimiento, 0.05)

    @patch('builtins.input', side_effect=['sí', '0.03', '0.06'])
    def test_configurar_tarifas_personalizadas(self, mock_input):
        self.taximetro.configurar_tarifas()
        self.assertEqual(self.taximetro.tarifa_parado, 0.03)
        self.assertEqual(self.taximetro.tarifa_movimiento, 0.06)

    def test_cambiar_estado_movimiento(self):
        tiempo_actual = time.time()
        self.taximetro._cambiar_estado(tiempo_actual, True)
        self.assertTrue(self.taximetro.en_movimiento)
        self.assertEqual(self.taximetro.tiempo_ultimo_cambio, tiempo_actual)

    def test_cambiar_estado_parado(self):
        tiempo_actual = time.time()
        self.taximetro._cambiar_estado(tiempo_actual, False)
        self.assertFalse(self.taximetro.en_movimiento)
        self.assertEqual(self.taximetro.tiempo_ultimo_cambio, tiempo_actual)

    def test_finalizar_carrera(self):
        self.taximetro.tiempo_movimiento = 120  # 2 minutos
        self.taximetro.tiempo_parado = 60       # 1 minuto
        self.taximetro.finalizar_carrera(time.time())
        # self.assertAlmostEqual(self.taximetro.total_euros, 3.30, places=2)
        self.assertEqual(round(self.taximetro.total_euros, 2), 3.30)

    def test_resetear_valores(self):
        self.taximetro.tiempo_movimiento = 120
        self.taximetro.tiempo_parado = 60
        self.taximetro.total_euros = 3.30
        self.taximetro.resetear_valores()
        self.assertEqual(self.taximetro.tiempo_movimiento, 0)
        self.assertEqual(self.taximetro.tiempo_parado, 0)
        self.assertEqual(self.taximetro.total_euros, 0)
        self.assertFalse(self.taximetro.en_movimiento)

if __name__ == "__main__":
    unittest.main()
