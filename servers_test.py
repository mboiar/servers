import unittest
from collections import Counter

from servers import ListServer, Product, Client, MapServer

server_types = (ListServer, MapServer)

class ProductTest(unittest.TestCase):
    def test_check_good_pattern_name(self):
        product_for_test = Product("AB123", 12.23)
        self.assertEqual(Product("AB123", 12.23), product_for_test)

    def test_check_bad_pattern_name(self):
        with self.assertRaises(ValueError):
            Product("12absd", 19.56)

        with self.assertRaises(ValueError):
            Product("1", 1.56)

        with self.assertRaises(ValueError):
            Product("z", 9.56)

    def test_check_bad_price(self):
        with self.assertRaises(ValueError):
            Product("bhy123", (-92.0))

        with self.assertRaises(ValueError):
            Product("Kud123", 0)



class ServerTest(unittest.TestCase):

    def test_get_entries_returns_proper_entries(self):
        products = [Product('P12', 1), Product('PP234', 2), Product('PP235', 1)]
        for server_type in server_types:
            server = server_type(products)
            entries = server.get_entries(2)
            self.assertEqual(Counter([products[2], products[1]]), Counter(entries))


class ClientTest(unittest.TestCase):
    def test_total_price_for_normal_execution(self):
        products = [Product('PP234', 2), Product('PP235', 3)]
        for server_type in server_types:
            server = server_type(products)
            client = Client(server)
            self.assertEqual(5, client.get_total_price(2))


if __name__ == '__main__':
    unittest.main()

