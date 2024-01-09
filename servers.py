#!/usr/bin/python
# -*- coding: utf-8 -*-
    
from typing import Optional, List, Union
import re

from abc import abstractmethod, ABC
    
    
class Product:
    # FIXME: klasa powinna posiadać metodę inicjalizacyjną przyjmującą argumenty wyrażające nazwę produktu (typu str) i jego cenę (typu float) -- w takiej kolejności -- i ustawiającą atrybuty `name` (typu str) oraz `price` (typu float)
    
    def __eq__(self, other):
        return None  # FIXME: zwróć odpowiednią wartość
    
    def __hash__(self):
        return hash((self.name, self.price))
    
class ServerError(Exception):
    pass
    
class TooManyProductsFoundError(ServerError):
    # Reprezentuje wyjątek związany ze znalezieniem zbyt dużej liczby produktów.
    pass


# FIXME: Każada z poniższych klas serwerów powinna posiadać:
#   (1) metodę inicjalizacyjną przyjmującą listę obiektów typu `Product` i ustawiającą atrybut `products` zgodnie z typem reprezentacji produktów na danym serwerze,
#   (2) możliwość odwołania się do atrybutu klasowego `n_max_returned_entries` (typu int) wyrażający maksymalną dopuszczalną liczbę wyników wyszukiwania,
#   (3) możliwość odwołania się do metody `get_entries(self, n_letters)` zwracającą listę produktów spełniających kryterium wyszukiwania

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
    
    def has_too_many_products(self, entries: List[Product]) -> bool:
        return len(entries) > Server.n_max_returned_entries
 

class ListServer(Server):
    def __init__(self, products: List[Product]) -> None:
        self.products_ = products

    def get_entries_(self, n_letters: int) -> List[Product]:
        return [p for p in self.products_ if self.match_product_name(p.name, n_letters)]
    
    
class MapServer(Server):
    def __init__(self, products: List[Product]) -> None:
        self.products_ = {p.name:p for p in products}

    def get_entries_(self, n_letters: int) -> [Product]:
        return [p[1] for p in self.products_.items() if self.match_product_name(p[0], n_letters)]


class Client:
    # FIXME: klasa powinna posiadać metodę inicjalizacyjną przyjmującą obiekt reprezentujący serwer
    
    def get_total_price(self, n_letters: Optional[int]) -> Optional[float]:
        raise NotImplementedError()

