from pathlib import Path
from typing import Optional

from pocketutils.tools.path_tools import PathTools

from mandos.model.searches import Search
from mandos.model.settings import SETTINGS
from mandos.model.utils.setup import logger


class EntryPaths:
    @classmethod
    def output_path_of(cls, what: Search, input_path: Path, to: Optional[Path]) -> Path:
        if to is None:
            return cls.default_path_of(what, input_path)
        elif str(to).startswith("."):
            return cls.default_path_of(what, input_path).with_suffix(str(to))
        else:
            return to

    @classmethod
    def default_path_of(cls, what: Search, input_path: Path) -> Path:
        parent = input_path.parent / (input_path.stem + "-output")
        child = what.key + SETTINGS.table_suffix
        node = PathTools.sanitize_path_node(child)
        if (parent / node).resolve() != (parent / child).resolve():
            logger.debug(f"Path {child} sanitized to {node}")
        return parent / node


__all__ = ["EntryPaths"]
