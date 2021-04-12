from __future__ import annotations

import os
import fnmatch
import re
import glob

from pathlib import Path
from dataclasses import dataclass
from typing import List, Tuple, Iterable

__author__ = "Giovanni Grano"
__license__ = "MIT"
__email__ = "grano@ifi.uzh.ch"


@dataclass
class Module:
    project_name: str
    name: str
    include_patterns: List[str]
    exclude_patterns: List[str]

    def __post_init__(self):
        self.include_patterns = [
            p.replace(".class", ".java") for p in self.include_patterns
        ]

    def find_cut_pairs(self, test_subdir: Path, src_subdir: Path) -> Iterable[CutPair]:
        tests = self.find_tests(test_subdir)
        return self.find_cuts(tests, src_subdir)

    def find_tests(self, test_subdir: Path) -> Iterable[Tuple[Path, str, str]]:
        excluded = {
            file
            for exclude in self.exclude_patterns
            for file in test_subdir.glob(exclude)
        }
        for include in self.include_patterns:
            for test_file in test_subdir.glob(include):
                if test_file not in excluded:
                    yield test_file, self.get_full_qualified_name(test_file), include

    def find_cuts(
        self, tests: Iterable[Tuple[Path, str, str]], src_subdir: Path
    ) -> Iterable[CutPair]:
        for test_path, test_qualified_name, include_pattern in tests:
            source_file_name = self.get_cut_name(test_path, include_pattern)
            for source_path in src_subdir.rglob(source_file_name):
                yield CutPair(
                    test_path,
                    test_qualified_name,
                    source_path,
                    self.get_full_qualified_name(source_path),
                )

    @staticmethod
    def get_cut_name(test_path: Path, include_pattern: str) -> str:
        """Returns the file name of the suspected class under test
        for a given test path and include pattern that found the test
        """
        if include_pattern.endswith("/*Test.java"):
            return re.sub(r"Test.java$", r".java", test_path.name)
        elif include_pattern.endswith("/Test*.java"):
            return re.sub(r"^Test", r"", test_path.name)
        elif include_pattern.endswith("/*TestCase.java"):
            return re.sub(r"TestCase.java$", r".java", test_path.name)
        else:
            return re.sub(
                r"(?:Test)?(.*?)(?:Test|TestCase)?\.java", r"\1.java", test_path.stem
            )

    @staticmethod
    def get_full_qualified_name(path: Path) -> str:
        with open(path, encoding="utf8", errors='ignore') as f:
            for line in f:
                if line.startswith('package'):
                    package = line.replace('package', '').strip().strip(';')
                    name = path.stem
                    return f"{package}.{name}"


@dataclass
class CutPair:
    test_path: Path
    test_qualified_name: str
    source_path: Path
    source_qualified_name: str
