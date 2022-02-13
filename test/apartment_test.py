from apartment import Apartment, Apartments, Price, Area, Year, Vastike, Floor, Rooms, Zone, K, Parameter
import pytest
import unittest

class TestParameter(unittest.TestCase):
    def test_K(self):
        self.assertEqual(K, 1000)

    def test_Parameter_Constructor_DefaultValues(self):
        p = Parameter(150*K)
        self.assertEqual(p.value, 150000)
        self.assertEqual(p.is_increasing_better, True)
        self.assertEqual(p.unit, "")
        self.assertEqual(p.name, "")
        self.assertEqual(p.range, None)
        self.assertEqual(p.weight, 1.0)
        self.assertEqual(p.normalized_value, 0.0)

    def test_Parameter_Throw_Errors(self):
        with pytest.raises(ValueError):
            p = Parameter(10, range=(100,10))

        with pytest.raises(ValueError):
            p = Parameter(0, range=(10,100))

    def test_Parameter_Constructor_CustomValues(self):
        p = Parameter(120*K, False, "euro", "price", (100*K, 400*K), 2.0)
        self.assertEqual(p.value, 120*K)
        self.assertEqual(p.is_increasing_better, False)
        self.assertEqual(p.unit, "euro")
        self.assertEqual(p.name, "price")
        self.assertEqual(p.range, (100*K, 400*K))


    def test_Price(self):
        price = Price(value=150 *K, range = None)
        self.assertEqual(price.is_increasing_better, False)
        self.assertEqual(price.value, 150 *K)
        self.assertEqual(price.normalized_value, 0.0)
        self.assertEqual(price.calculate_weighted_value(), 0.0)

        price.normalize(150*K, 350*K)
        self.assertEqual(price.normalized_value, 1.0)
        self.assertEqual(price.calculate_weighted_value(), 1.0)

        price.normalize(100*K, 200*K)
        self.assertEqual(price.normalized_value, 0.5)
        self.assertEqual(price.calculate_weighted_value(), 0.5)
