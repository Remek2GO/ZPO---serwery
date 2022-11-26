#!/usr/bin/python
# -*- coding: utf-8 -*-
 
from typing import Optional, List, Dict
from abc import ABC, abstractmethod
import re
 
# FIXME: Każada z poniższych klas serwerów powinna posiadać:
#   (1) metodę inicjalizacyjną przyjmującą listę obiektów typu `Product` i ustawiającą atrybut `products` zgodnie z typem reprezentacji produktów na danym serwerze,
#   (2) możliwość odwołania się do atrybutu klasowego `n_max_returned_entries` (typu int) wyrażający maksymalną dopuszczalną liczbę wyników wyszukiwania,
#   (3) możliwość odwołania się do metody `get_entries(self, n_letters)` zwracającą listę produktów spełniających kryterium wyszukiwania

class ServerError(Exception):
    pass 

class TooManyProductsFoundError(ServerError):
    # Reprezentuje wyjątek związany ze znalezieniem zbyt dużej liczby produktów.
    pass


class Server(ABC): #klasa abstrakcyjna
    n_max_returned_entries = 3

    def __init__(self, *args, **kwargs) -> None:
         super().__init__()

    def get_entries(self, n_letters) -> List[Product]: #ogólna metoda zwracająca listę produktów na podstawie zadanej liczby liter 
        characters = '^[a-zA-Z]{{{n}}}\\d{{2,3}}$'.format(n=n_letters)
        entries = []
        for i in self._get_products(n_letters):
            if re.match(characters,i.name): #sprawdzenie czy spełniają kryterium
                entries.append(i)
            if len(entries) > Server.n_max_returned_entries:
                return TooManyProductsFoundError

        return sorted(entries, key = lambda entry: entry.price) #sortowanie względem ceny produktu


    @abstractmethod #dostarcza niezbędnych danych metodzie wyżej
    def _get_products(self,n_letters: int = 1)-> List[Product]:
        raise NotImplementedError



class ListServer(Server):

    def __init__(self, products: List[Product], *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.products: List[Product] = products

    def _get_products(self, n_letters: int = 1) -> List[Product]:
        return self.products
 
class MapServer(Server):

    def __init__(self, products: List[Product], *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.products: Dict[str, Product] = {p.name: p for p in products}
        
    def _get_products(self, products: List[Product], n_letters: int = 1) -> List[Product]:
        return list(self.products.values())
