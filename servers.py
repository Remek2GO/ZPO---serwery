#!/usr/bin/python
# -*- coding: utf-8 -*-
 
from typing import Optional, List, Dict, TypeVar
from abc import  ABC, abstractmethod
import re
from re import match


class ServerError(Exception):
    pass 

class TooManyProductsFoundError(Exception):
    # Reprezentuje wyjątek związany ze znalezieniem zbyt dużej liczby produktów.
    pass

class Product:
    def __init__(self, name: str, price: float) -> None: #metoda inicjalizacyjna
        if not isinstance(name,str):
            raise ValueError('Name should be created only with string')
        if not isinstance(price, (int, float)):
            raise ValueError('Price should be float or int')
        if not re.fullmatch(r'^[a-zA-Z]+\d+$',name):
            raise ValueError('Name should be changed to letters and numbers')
        self.name = name
        self.price = price

    def __str__(self):
        return "Nazwa: {0} Cena: {1}".format(self.name, self.price)

    def __eq__(self, other):
        return self.name == other.name and self.price == other.price

    def __hash__(self):
        return hash((self.name, self.price))

    def get_price(self):
        return self.price

    def get_name(self):
        return self.name

n_letters = int
n_max_returned_entries = int

class Server(ABC): #klasa abstrakcyjna
    n_max_returned_entries = 3
    def __init__(self, list_product: List[Product]):
        self.list_product = list_product

    @abstractmethod
    def get_entries(self, n_letters = 1):
        pass

    @classmethod
    def checklenght(cls, list):
        if len(list) > cls.n_max_returned_entries:
            raise TooManyProductsFoundError('Too many products were found')
        pass


class Client:
    def __init__(self,client_server: Server):
        self.client_server = client_server
    def get_total_price(self, n_letters: Optional[int]) -> Optional[float]:
        total_price=0.0
        try:
            l_product = self.client_server.get_entries(n_letters)
            if len(l_product) == 0:
                return None
            else:
                for product in l_product:
                    total_price = total_price + product.price
            return total_price
        except TooManyProductsFoundError:
            return None

class ListServer(Server):

    def __init__(self, list_product: List[Product]):
        super().__init__(list_product)
        self.list = self.list_product

    def get_entries(self,n_letters = 1):
        outcome = []
        for obj in self.list:
            name = obj.name
            result = match('^[a-zA-Z]{{{n}}}\\d{{2,3}}$'.format(n=n_letters),name)
            if result is not None:
                outcome.append(obj)

        ListServer.checklenght(outcome)

        outcome.sort(key = lambda a: a.get_price())

        return outcome
 
class MapServer(Server):

    def __init__(self, list_product: List[Product]):
        super().__init__(list_product)
        self.dic = {obj.name: obj for obj in self.list_product }

    def get_entries(self,n_letters = 1):
        outcome = []
        for key, obj in self.dic.items():
            result = match('^[a-zA-Z]{{{n}}}\\d{{2,3}}$'.format(n=n_letters), key)
            if result is not None:
                outcome.append(obj)

        MapServer.checklenght(outcome)

        outcome.sort(key = lambda a: a.get_price())

        return outcome
