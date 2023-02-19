from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(eq=True, frozen=True)
class Currency:
    name:str
