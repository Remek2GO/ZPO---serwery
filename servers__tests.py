import unittest

from ostateczna_wersj_serwus import Server, ListServer, Product, Client, TooManyProductsFoundError, MapServer

server_types = (ListServer, MapServer)

class ServerTest(unittest.TestCase):
    def test_get_entries_returns_sorted_results(self):
        products = [Product('P12', 1), Product('PP234', 2), Product('PP235', 1)]
        server = ListServer(products)
        entries = server.get_entries(3)

        self.assertListEqual([], entries)
        print(entries)

   


class TestClient(unittest.TestCase):
    def test_total_price_is_zero_if_exception_raised(self):
        products = [Product('PP234', 2)] * (Server.n_max_returned_entries + 1)
        server = ListServer(products)
        client = Client(server)

        self.assertEqual(0, client.get_total_price(2))


if __name__ == '__main__':
    unittest.main()
