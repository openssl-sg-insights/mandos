import abc
from dataclasses import dataclass
from typing import Any, Mapping, Type, TypeVar

from pocketutils.core.dot_dict import NestedDotDict

from mandos.model import MiscUtils
from mandos.model.apis.pubchem_api import PubchemApi
from mandos.model.apis.pubchem_support.pubchem_data import PubchemData
from mandos.model.hits import AbstractHit
from mandos.model.searches import Search

H = TypeVar("H", bound=AbstractHit, covariant=True)


@dataclass(frozen=True, order=True, repr=True)
class PubchemHit(AbstractHit, metaclass=abc.ABCMeta):
    """ """


class PubchemSearch(Search[H], metaclass=abc.ABCMeta):
    def __init__(self, key: str, api: PubchemApi):
        """
        Constructor.

        Args:
            api:
        """
        if api is None:
            raise ValueError(self.__class__.__name__)
        super().__init__(key)
        self.api = api


__all__ = ["PubchemHit", "PubchemSearch"]
