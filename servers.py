#!/usr/bin/python
# -*- coding: utf-8 -*-
    
from typing import Optional, List, Union, Self
import re

from abc import abstractmethod, ABC

    
class Product:
    def __init__(self, name: str, price: Union[float, int]) -> None:
        # Check the types
        if not (isinstance(name, str) and isinstance(price, (int, float))):
            raise ValueError("The name or price is wrong type!")
        elif not re.findall(r'^[A-Za-z]+\d+$', name):
            raise ValueError("The name have bad pattern!")
        elif price <= 0:
            raise ValueError("The price is bad!")
        else:
            self.name = name
            self.price = price

    def __eq__(self, other: Self):
        return self.__hash__() == other.__hash__()

    def __hash__(self):
        return hash((self.name, self.price))


class ServerError(Exception):
    pass  


class TooManyProductsFoundError:
    # Reprezentuje wyjątek związany ze znalezieniem zbyt dużej liczby produktów.
    pass
    
    
class Server(ABC):
    n_max_returned_entries = 3

    @abstractmethod
    def __init__(self, products: List[Product]) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_entries_(self, n_letters: int) -> List[Product]:
        raise NotImplementedError
    
    def get_entries(self, n_letters: int) -> List[Product]:
        entries = self.get_entries_(n_letters)
        if entries is None:
            return []
        elif Server.has_too_many_products(entries):
            raise TooManyProductsFoundError(f"Liczba znalezionych produktów przekracza maks. wartość: {len(entries)} > {Server.n_max_returned_entries}")
        else:
            return sorted(entries, key=lambda p: p.price)
    
    def match_product_name(self, product: Product, n_letters: int) -> Union[re.Match, None]:
        return re.fullmatch(f'^[a-zA-Z]{{{n_letters}}}\\d{{2,3}}$', product.name)
    
    def has_too_many_products(entries: List[Product]) -> bool:
        return len(entries) > Server.n_max_returned_entries
 

class ListServer(Server):
    def __init__(self, products: List[Product]) -> None:
        self.products_ = products

    def get_entries_(self, n_letters: int) -> List[Product]:
        return [p for p in self.products_ if self.match_product_name(p, n_letters)]
    
    
class MapServer(Server):
    def __init__(self, products: List[Product]) -> None:
        self.products_ = {p.name:p for p in products}

    def get_entries_(self, n_letters: int) -> [Product]:
        return [p[1] for p in self.products_.items() if self.match_product_name(p[1], n_letters)]


class Client:
    # FIXME: klasa powinna posiadać metodę inicjalizacyjną przyjmującą obiekt reprezentujący serwer
    
    def __init__(self, server: Server):
        self.server = server

    def get_total_price(self, n_letters: Optional[int]) -> Optional[float]:
        sum = 0
        try:
            entries: list = self.server.get_entries(n_letters)
            if not entries:
                raise Exception("a list is empty")
            for e in entries:
                sum += e.price
        except:
            return None
        else:
            return sum
