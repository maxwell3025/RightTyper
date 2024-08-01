from typing import FrozenSet, Set, Tuple

import libcst as cst

from righttyper.get_import_details import (
    generate_import_nodes,
)
from righttyper.righttyper_types import Filename


class ConstructImportTransformer(cst.CSTTransformer):
    def __init__(
        self,
        imports: Set[
            Tuple[
                Filename,
                Filename,
                str,
                Tuple[
                    str,
                    FrozenSet[str],
                    str,
                    FrozenSet[str],
                ],
            ]
        ],
        root_path: str,
    ) -> None:
        self.imports = imports
        self.root_path = root_path

    def leave_Module(
        self,
        original_node: cst.Module,
        updated_node: cst.Module,
    ) -> cst.Module:
        new_imports = []  # set()

        # import site
        # import sysconfig

        # Paths to the main and user libraries, with an os separator added
        # Used to generate import statements later.
        # purelib = sysconfig.get_paths()["purelib"]
        # platstdlib = sysconfig.get_paths()["platstdlib"]
        # userlib = site.getusersitepackages()

        for (
            function_file_path,
            class_file_path,
            class_name,
            import_details,
        ) in self.imports:
            q = generate_import_nodes(import_details)
            new_imports.extend(q)

        # Add all import statements at the beginning of the module
        return updated_node.with_changes(
            body=list(new_imports) + list(updated_node.body)
        )