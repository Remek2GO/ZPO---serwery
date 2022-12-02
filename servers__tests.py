#!/usr/bin/python
# -*- coding: utf-8 -*-

import unittest
from collections import Counter

from servers import ListServer, Product, Client, MapServer, TooManyProductsFoundError

server_types = (ListServer, MapServer)


class ServerTest(unittest.TestCase):
    def test_get_entries_returns_proper_entries(self):
        products = [Product('P12', 1), Product('PP234', 2), Product('PP235', 1)]
        for server_type in server_types:
            server = server_type(products)
            entries1 = server.get_entries(1)
            entries2 = server.get_entries(2)
            entries3 = server.get_entries(3)

            self.assertEqual(Counter([products[0]]), Counter(entries1))
            self.assertEqual(Counter([products[2], products[1]]), Counter(entries2))
            self.assertEqual(Counter([]), Counter(entries3))
        products_error_test = [Product('P12', 1), Product('P245', 2), Product('c56', 2), Product('x88', 1)]
        for server_type in server_types:
            server = server_type(products_error_test)
            with self.assertRaises(TooManyProductsFoundError):
                server.get_entries(1)

class ClientTest(unittest.TestCase):
    def test_total_price_for_normal_execution(self):
        products = [Product('PP234', 2), Product('PP235', 3)]
        for server_type in server_types:
            server = server_type(products)
            client = Client(server)
            self.assertEqual(5, client.get_total_price(2))
            self.assertEqual(None, client.get_total_price(1))
            self.assertEqual(None, client.get_total_price(4))


if __name__ == '__main__':
    unittest.main()