#!/usr/bin/python
# -*- coding: utf-8 -*-
 
from typing import Optional, List, Dict
from abc import TypeVar, ABC, abstractmethod
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

class Product:
    def __init__(self, name: str, price: float) -> None: #metoda inicjalizacyjna
        if name.isdigit() or name.isalpha() or name == None: # sprawdzam czy nazwa jest poprawna
            raise ValueError
        self.name: str = name
        self.price: float = price

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

ServerType = TypeVar('ServerType', bound=Server) #Użycie TypeVar aby otrzymać ten sam typ serwera


class Client:
    def __init__(self, server: ServerType) -> None: # metoda inicjalizacyjna
        self.server: ServerType = server

    def get_total_price(self, n_letters: Optional[int]) -> float:
        try:
            entries = self.server.get_entries() if n_letters is None \
                else self.server.get_entries(n_letters)
            return sum([entry.price for entry in entries])
        except TooManyProductsFoundError:
            return 0

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
