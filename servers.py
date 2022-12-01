#!/usr/bin/python
# -*- coding: utf-8 -*-
 
from typing import Optional, List, Dict, TypeVar
from abc import  ABC, abstractmethod
import re





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


    def get_entries(self, n_letters: int = 1) -> List[Product]:
        pattern = '^[a-zA-Z]{{{n_letters}}}\\d{{2,3}}$'.format(n_letters=n_letters)
        entries = [p for p in self._get_products(n_letters)
                   if re.match(pattern, p.name)]
        if len(entries) > Server.n_max_returned_entries:
            raise TooManyProductsFoundError
        return sorted(entries, key=lambda entry: entry.price) #sortowanie względem ceny produktu
    

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
