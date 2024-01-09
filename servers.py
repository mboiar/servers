#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
from typing import Optional, Self


class Product:
    def __init__(self, name: str, price: float) -> None:
        # Check the types
        if not (isinstance(name, str) and isinstance(price, float)):
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


class TooManyProductsFoundError:
    # Reprezentuje wyjątek związany ze znalezieniem zbyt dużej liczby produktów.
    pass


# FIXME: Każda z poniższych klas serwerów powinna posiadać:
#   (1) metodę inicjalizacyjną przyjmującą listę obiektów typu `Product` i ustawiającą atrybut `products` zgodnie z
#   typem reprezentacji produktów na danym serwerze,
#   (2) możliwość odwołania się do atrybutu klasowego `n_max_returned_entries` (typu int) wyrażający maksymalną
#   dopuszczalną liczbę wyników wyszukiwania,
#   (3) możliwość odwołania się do metody `get_entries(self, n_letters)` zwracającą listę produktów spełniających
#   kryterium wyszukiwania

class ListServer:
    pass


class MapServer:
    pass


class Client:
    # FIXME: klasa powinna posiadać metodę inicjalizacyjną przyjmującą obiekt reprezentujący serwer

    def get_total_price(self, n_letters: Optional[int]) -> Optional[float]:
        raise NotImplementedError()
