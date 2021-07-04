from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence, Set

from pocketutils.core.dot_dict import NestedDotDict

from mandos.model import MiscUtils
from mandos.model.apis.chembl_api import ChemblApi
from mandos.model.apis.chembl_support import ChemblCompound
from mandos.model.apis.chembl_support.chembl_utils import ChemblUtils
from mandos.search.chembl import ChemblHit, ChemblSearch


@dataclass(frozen=True, order=True, repr=True)
class AtcHit(ChemblHit):
    """
    An ATC code found for a compound.
    """

    level: int


class AtcSearch(ChemblSearch[AtcHit]):
    """ """

    def __init__(self, key: str, levels: Set[int], api: ChemblApi):
        super().__init__(key, api)
        self.levels = levels

    @property
    def data_source(self) -> str:
        return "ChEMBL :: ATC codes"

    def find(self, lookup: str) -> Sequence[AtcHit]:
        """

        Args:
            lookup:

        Returns:

        """
        # 'atc_classifications': ['S01HA01', 'N01BC01', 'R02AD03', 'S02DA02']
        # 'indication_class': 'Anesthetic (topical)'
        ch = ChemblUtils(self.api).get_compound_dot_dict(lookup)
        compound = ChemblUtils(self.api).compound_dot_dict_to_obj(ch)
        hits = []
        if "atc_classifications" in ch:
            for atc in ch["atc_classifications"]:
                hits.extend(self.process(lookup, compound, atc))
        return hits

    def process(self, lookup: str, compound: ChemblCompound, atc: str) -> Sequence[AtcHit]:
        """

        Args:
            lookup:
            compound:
            atc:

        Returns:

        """
        dots = NestedDotDict(self.api.atc_class.get(atc))
        found = []
        for level in sorted(self.levels):
            found.append(self._code(lookup, compound, dots, level))
        return found

    def _code(self, lookup: str, compound: ChemblCompound, dots: NestedDotDict, level: int):
        # 'level1': 'N', 'level1_description': 'NERVOUS SYSTEM', 'level2': 'N05', ...
        # Unfortunately ChEMBL doesn't contain the exact compound names for ATC
        # TODO: These names do not exactly match what ATC uses
        if level == 5:
            object_name = compound.name.lower()
        else:
            object_name = dots.get(f"level{level}_description")
        return self._create_hit(
            c_origin=lookup,
            c_matched=compound.inchikey,
            c_id=compound.chid,
            c_name=compound.name,
            predicate=f"atc:level{level}",
            statement=f"has ATC level {level} code",
            object_id=dots.get(f"level{level}"),
            object_name=object_name,
            level=level,
        )


__all__ = ["AtcHit", "AtcSearch"]
