#!/usr/bin/python
# -*- coding: utf-8 -*-

from typing import Optional, List, Union, TypeVar
import re

from abc import abstractmethod, ABC


class Product:
    def __init__(self, name: str, price: Union[float, int]) -> None:
        # Check the types
        if not (isinstance(name, str) and isinstance(price, (int, float))):
            raise ValueError("The name or price is wrong type!")
        elif not re.findall(r'^[A-Za-z]+\d+$', name):
            raise ValueError("The name have bad pattern!")
        else:
            self.name = name
            self.price = price

    def __eq__(self, other: "Product"):
        return self.__hash__() == other.__hash__()

    def __hash__(self):
        return hash((self.name, self.price))


class ServerError(Exception):
    pass


class TooManyProductsFoundError(ServerError):
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

    @staticmethod
    def match_product_name(product: Product, n_letters: int) -> Union[re.Match, None]:
        return re.fullmatch(f'^[a-zA-Z]{{{n_letters}}}\\d{{2,3}}$', product.name)

    @staticmethod
    def has_too_many_products(entries: List[Product]) -> bool:
        return len(entries) > Server.n_max_returned_entries


ServerType = TypeVar("ServerType", bound=Server)


class ListServer(Server):
    def __init__(self, products: List[Product]) -> None:
        self.products = products

    def get_entries_(self, n_letters: int) -> List[Product]:
        return [p for p in self.products if self.match_product_name(p, n_letters)]


class MapServer(Server):
    def __init__(self, products: List[Product]) -> None:
        self.products = {p.name:p for p in products}

    def get_entries_(self, n_letters: int) -> [Product]:
        return [p[1] for p in self.products.items() if self.match_product_name(p[1], n_letters)]


class Client:
    # FIXME: klasa powinna posiadać metodę inicjalizacyjną przyjmującą obiekt reprezentujący serwer

    def __init__(self, server: ServerType):
        self.server = server

    def get_total_price(self, n_letters: Optional[int]) -> Optional[float]:
        sum_ = 0
        try:
            entries = self.server.get_entries(n_letters)
            if not entries:
                return None
            for e in entries:
                sum_ += e.price
        except ServerError:
            return None
        else:
            return sum_
